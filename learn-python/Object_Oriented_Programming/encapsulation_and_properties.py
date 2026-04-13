"""
Encapsulation and properties in Python.
"""

class Temperature:
    """Demonstrates encapsulation with properties."""

    def __init__(self, celsius=0):
        self._celsius = celsius  # protected by convention

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9

    @property
    def kelvin(self):
        return self._celsius + 273.15

    def __repr__(self):
        return f"Temperature({self._celsius}°C)"


class User:
    """Demonstrates name mangling and access control."""

    def __init__(self, username, password):
        self.username = username
        self.__password = password  # name-mangled
        self._email = None

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if '@' not in value:
            raise ValueError("Invalid email")
        self._email = value

    def verify_password(self, password):
        return self.__password == password

    def _internal_method(self):
        """Convention: not part of public API."""
        return "internal"


class ImmutablePoint:
    """Read-only properties using __slots__ and properties."""
    __slots__ = ('_x', '_y')

    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __repr__(self):
        return f"ImmutablePoint({self._x}, {self._y})"


if __name__ == "__main__":
    # Temperature
    t = Temperature(100)
    print(f"{t}: {t.fahrenheit}°F, {t.kelvin}K")
    t.fahrenheit = 32
    print(f"After setting 32°F: {t}")

    try:
        t.celsius = -300
    except ValueError as e:
        print(f"Error: {e}")

    # User
    user = User("alice", "secret123")
    user.email = "alice@example.com"
    print(f"\nUser: {user.username}, email: {user.email}")
    print(f"Password correct: {user.verify_password('secret123')}")

    # Name mangling access (not recommended)
    print(f"Mangled name: {user._User__password}")

    # Immutable
    point = ImmutablePoint(3, 4)
    print(f"\n{point}")
    try:
        point.x = 10
    except AttributeError as e:
        print(f"Cannot modify: {e}")
