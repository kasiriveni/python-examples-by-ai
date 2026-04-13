"""
Operator overloading in Python.
"""

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # String representations
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"

    # Arithmetic operators
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __abs__(self):
        return (self.x**2 + self.y**2) ** 0.5

    # Comparison operators
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return abs(self) < abs(other)

    def __le__(self, other):
        return abs(self) <= abs(other)

    # Container-like behavior
    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        raise IndexError(f"Index {index} out of range")

    def __len__(self):
        return 2

    def __iter__(self):
        yield self.x
        yield self.y

    # Callable
    def __call__(self, scalar):
        return self * scalar

    # Boolean
    def __bool__(self):
        return self.x != 0 or self.y != 0

    # Dot product
    def dot(self, other):
        return self.x * other.x + self.y * other.y


if __name__ == "__main__":
    v1 = Vector(3, 4)
    v2 = Vector(1, 2)

    print(f"v1 = {v1}")
    print(f"v2 = {v2}")
    print(f"v1 + v2 = {v1 + v2}")
    print(f"v1 - v2 = {v1 - v2}")
    print(f"v1 * 3 = {v1 * 3}")
    print(f"3 * v1 = {3 * v1}")
    print(f"-v1 = {-v1}")
    print(f"|v1| = {abs(v1)}")
    print(f"v1 == v2: {v1 == v2}")
    print(f"v1 < v2: {v1 < v2}")
    print(f"v1[0] = {v1[0]}, v1[1] = {v1[1]}")
    print(f"len(v1) = {len(v1)}")
    print(f"list(v1) = {list(v1)}")
    print(f"v1(2) = {v1(2)}")
    print(f"v1.dot(v2) = {v1.dot(v2)}")
    print(f"bool(Vector(0,0)) = {bool(Vector(0, 0))}")
