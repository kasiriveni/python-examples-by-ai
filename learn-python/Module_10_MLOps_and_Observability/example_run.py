"""Example runner for Module 10: MLOps & Observability (metadata write)"""
import json
import tempfile
import os


def main():
    print("Module 10 - MLOps example")
    metadata = {"model": "toy-model", "version": "0.1", "accuracy": 0.92}
    fd, path = tempfile.mkstemp(prefix="model_meta_", suffix=".json")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(metadata, f)
    print("Wrote metadata to", path)


if __name__ == "__main__":
    main()
