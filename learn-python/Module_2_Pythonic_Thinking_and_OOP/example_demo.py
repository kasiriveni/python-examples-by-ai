"""Pythonic Thinking & OOP demo: dataclass and typing example"""
from dataclasses import dataclass
from typing import List


@dataclass
class Point:
    x: float
    y: float


def centroid(points: List[Point]) -> Point:
    sx = sum(p.x for p in points) / len(points)
    sy = sum(p.y for p in points) / len(points)
    return Point(sx, sy)


def main():
    pts = [Point(0, 0), Point(1, 1), Point(2, 0)]
    c = centroid(pts)
    print("Points:", pts)
    print("Centroid:", c)


if __name__ == '__main__':
    main()
