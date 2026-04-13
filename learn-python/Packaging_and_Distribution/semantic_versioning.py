"""
Packaging and Distribution: Semantic versioning and changelog management.
"""
import re
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Iterator

# ═══════════════════════════════════════════
# 1. Semantic version (SemVer)
# ═══════════════════════════════════════════
class BumpType(Enum):
    MAJOR = auto()
    MINOR = auto()
    PATCH = auto()
    PRE   = auto()

@dataclass(order=True, frozen=True)
class Version:
    """Semantic Version: MAJOR.MINOR.PATCH[-pre][+build]"""
    major: int = 0
    minor: int = 0
    patch: int = 0
    pre:   str = ""     # e.g. "alpha.1", "beta.2", "rc.1"
    build: str = ""     # e.g. "build.001"

    # Sort key: ignore build; pre-releases come before release
    def __lt__(self, other: "Version") -> bool:
        s = (self.major, self.minor, self.patch)
        o = (other.major, other.minor, other.patch)
        if s != o:
            return s < o
        # pre-release < release
        if self.pre and not other.pre: return True
        if not self.pre and other.pre: return False
        return self.pre < other.pre

    def __str__(self) -> str:
        v = f"{self.major}.{self.minor}.{self.patch}"
        if self.pre:   v += f"-{self.pre}"
        if self.build: v += f"+{self.build}"
        return v

    def bump(self, bump_type: BumpType, pre: str = "") -> "Version":
        if bump_type == BumpType.MAJOR:
            return Version(self.major + 1, 0, 0)
        if bump_type == BumpType.MINOR:
            return Version(self.major, self.minor + 1, 0)
        if bump_type == BumpType.PATCH:
            return Version(self.major, self.minor, self.patch + 1)
        return Version(self.major, self.minor, self.patch, pre)

    def is_stable(self) -> bool:
        return self.major >= 1 and not self.pre

    def is_compatible_with(self, other: "Version") -> bool:
        """Return True if self is backward-compatible with other (same major)."""
        return self.major == other.major and self >= other

    @staticmethod
    def parse(version_str: str) -> "Version":
        _SEMVER_RE = re.compile(
            r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
            r"(?:-(?P<pre>[a-zA-Z0-9.]+))?(?:\+(?P<build>[a-zA-Z0-9.]+))?$"
        )
        m = _SEMVER_RE.match(version_str.strip())
        if not m:
            raise ValueError(f"Invalid semver: {version_str!r}")
        return Version(
            int(m["major"]), int(m["minor"]), int(m["patch"]),
            m["pre"] or "", m["build"] or "",
        )

# ═══════════════════════════════════════════
# 2. Changelog entry types
# ═══════════════════════════════════════════
class ChangeType(str, Enum):
    ADDED      = "Added"
    CHANGED    = "Changed"
    DEPRECATED = "Deprecated"
    REMOVED    = "Removed"
    FIXED      = "Fixed"
    SECURITY   = "Security"

@dataclass
class ChangeEntry:
    change_type: ChangeType
    description: str
    issue: str = ""       # e.g. "#123"
    pr:    str = ""       # e.g. "#456"

    def __str__(self) -> str:
        suffix_parts = []
        if self.issue: suffix_parts.append(f"Issue {self.issue}")
        if self.pr:    suffix_parts.append(f"PR {self.pr}")
        suffix = f" ({', '.join(suffix_parts)})" if suffix_parts else ""
        return f"- {self.description}{suffix}"

@dataclass
class Release:
    version: Version
    date: str
    entries: list[ChangeEntry] = field(default_factory=list)
    yanked: bool = False

    def add(self, change_type: ChangeType, desc: str,
            issue: str = "", pr: str = "") -> "Release":
        self.entries.append(ChangeEntry(change_type, desc, issue, pr))
        return self

    def determine_bump(self) -> BumpType:
        """Determine version bump type from entries (conventional commits style)."""
        types = {e.change_type for e in self.entries}
        if ChangeType.REMOVED in types:
            return BumpType.MAJOR
        if ChangeType.ADDED in types or ChangeType.CHANGED in types:
            return BumpType.MINOR
        return BumpType.PATCH

    def to_markdown(self) -> str:
        lines = []
        marker = " [YANKED]" if self.yanked else ""
        lines.append(f"## [{self.version}]{marker} - {self.date}\n")
        from itertools import groupby
        sorted_entries = sorted(self.entries, key=lambda e: e.change_type.value)
        for ct, group in groupby(sorted_entries, key=lambda e: e.change_type):
            lines.append(f"### {ct.value}\n")
            for entry in group:
                lines.append(str(entry))
            lines.append("")
        return "\n".join(lines)

@dataclass
class Changelog:
    project: str
    description: str = ""
    releases: list[Release] = field(default_factory=list)

    def add_release(self, release: Release) -> "Changelog":
        self.releases.append(release)
        self.releases.sort(key=lambda r: r.version, reverse=True)
        return self

    def latest(self) -> Release | None:
        return self.releases[0] if self.releases else None

    def to_markdown(self) -> str:
        lines = [
            f"# Changelog — {self.project}\n",
            "All notable changes to this project will be documented here.\n",
            "Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)\n",
            "Versioning: [Semantic Versioning](https://semver.org/)\n",
            "---\n",
        ]
        if self.releases:
            lines.append("## [Unreleased]\n")
            for release in self.releases:
                lines.append(release.to_markdown())
        return "\n".join(lines)

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_markdown())
        print(f"Changelog written to {path}")

# ═══════════════════════════════════════════
# 3. Version constraint checker
# ═══════════════════════════════════════════
def parse_requirement(req: str) -> tuple[str, str]:
    """Parse 'package>=1.0.0' → ('package', '>=1.0.0')"""
    m = re.match(r'^([\w\-\.]+)\s*([><=!~^].+)?$', req.strip())
    if not m:
        raise ValueError(f"Invalid requirement: {req}")
    return m.group(1), m.group(2) or ""

def satisfies(version: Version, constraint: str) -> bool:
    """Check if version satisfies a constraint like '>=1.2.0,<2.0.0'."""
    if not constraint.strip():
        return True
    for part in constraint.split(","):
        part = part.strip()
        m = re.match(r'^([><=!~^]{1,2})([\d.]+(?:-\w[\w.]*)?)$', part)
        if not m:
            raise ValueError(f"Invalid constraint: {part!r}")
        op, ver_str = m.group(1), m.group(2)
        # Pad to x.y.z
        parts = ver_str.split(".")
        while len(parts) < 3: parts.append("0")
        target = Version.parse(".".join(parts[:3]))

        result = {
            ">=": version >= target,
            ">":  version >  target,
            "<=": version <= target,
            "<":  version <  target,
            "==": version == target,
            "!=": version != target,
            "~=": (version >= target and version.major == target.major
                   and version.minor == target.minor),
            "^":  (version >= target and version.major == target.major),
        }.get(op)

        if result is None:
            raise ValueError(f"Unknown operator: {op}")
        if not result:
            return False
    return True

if __name__ == "__main__":
    print("=== Semantic Versioning ===")
    v1 = Version.parse("1.2.3")
    v2 = Version.parse("2.0.0-rc.1")
    v3 = Version.parse("1.2.4")
    v4 = Version.parse("1.2.3-alpha.1")

    for v in sorted([v1, v2, v3, v4]):
        print(f"  {str(v):25s} stable={v.is_stable()}")

    print(f"\n  Bumping {v1}:")
    print(f"    major → {v1.bump(BumpType.MAJOR)}")
    print(f"    minor → {v1.bump(BumpType.MINOR)}")
    print(f"    patch → {v1.bump(BumpType.PATCH)}")
    print(f"    pre   → {v1.bump(BumpType.PRE, 'beta.1')}")

    print(f"\n  {v3} compatible with {v1}: {v3.is_compatible_with(v1)}")
    print(f"  {v2} compatible with {v1}: {v2.is_compatible_with(v1)}")

    print("\n=== Version Constraints ===")
    tests = [
        ("1.5.0", ">=1.0.0,<2.0.0"),
        ("2.0.0", ">=1.0.0,<2.0.0"),
        ("1.2.3", "==1.2.3"),
        ("1.2.4", "~=1.2.3"),
        ("1.3.0", "~=1.2.3"),
        ("1.9.0", "^1.0.0"),
        ("2.0.0", "^1.0.0"),
    ]
    for ver_s, constraint in tests:
        v = Version.parse(ver_s)
        ok = satisfies(v, constraint)
        print(f"  {ver_s:10s} {constraint:20s} → {'✓' if ok else '✗'}")

    print("\n=== Changelog ===")
    cl = Changelog("mypackage", "A demo Python package")

    r100 = Release(Version(1, 0, 0), "2023-01-15")
    r100.add(ChangeType.ADDED, "Initial public release", pr="#1")
    r100.add(ChangeType.ADDED, "Basic CLI interface")

    r110 = Release(Version(1, 1, 0), "2023-06-01")
    r110.add(ChangeType.ADDED, "New --verbose flag", issue="#45", pr="#50")
    r110.add(ChangeType.FIXED, "Memory leak in parser", issue="#38")
    r110.add(ChangeType.SECURITY, "Updated dependency versions")

    r111 = Release(Version(1, 1, 1), "2023-07-10")
    r111.add(ChangeType.FIXED, "Crash when config is empty", issue="#55")

    cl.add_release(r100).add_release(r110).add_release(r111)

    print(cl.to_markdown())
    print(f"  Latest version: {cl.latest().version}")
    print(f"  Suggested next bump type: {r110.determine_bump().name}")
