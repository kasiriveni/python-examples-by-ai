"""Production demo: simple retry decorator and usage"""
import time


def retry(times=3, backoff=0.05):
    def _decor(fn):
        def wrapper(*a, **k):
            for i in range(times):
                try:
                    return fn(*a, **k)
                except Exception as e:
                    if i == times - 1:
                        raise
                    time.sleep(backoff)
        return wrapper
    return _decor


@retry(times=2, backoff=0.01)
def sometimes_fails(x):
    if x < 0:
        raise ValueError("negative")
    return x * 2


def main():
    print("Production retry demo")
    print(sometimes_fails(3))


if __name__ == '__main__':
    main()
