"""MLOps demo: save/load simple model metadata to file"""
import json
import os


def save_meta(path, meta):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(meta, f)


def load_meta(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    print("MLOps demo")
    p = 'tmp_meta.json'
    meta = {'name': 'toy', 'v': 1}
    save_meta(p, meta)
    print('Saved', load_meta(p))
    try:
        os.remove(p)
    except Exception:
        pass


if __name__ == '__main__':
    main()
