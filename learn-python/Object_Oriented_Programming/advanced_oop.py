# Advanced OOP: metaclass and __slots__
class SlotMeta(type):
    def __new__(mcls, name, bases, ns):
        ns.setdefault('__slots__', ())
        return super().__new__(mcls, name, bases, ns)

class Base(metaclass=SlotMeta):
    __slots__ = ('x',)
    def __init__(self, x):
        self.x = x

b = Base(5)
print(b.x)
