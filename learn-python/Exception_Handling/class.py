# class example

# class MyClass:
#     def __init__(self, value):
#         self.value = value

#     def display(self):
#         print(f'The value is: {self.value}')

# obj = MyClass(10)
# print(obj.display())
# print(obj.value)


# example public and private mthods

class MyClass:
    def __init__(self, value):
        self.value = value

    def public_method(self):
        print('This is a public method')
        self.__private_method()

    def __private_method(self):
        print('This is a private method')


obj = MyClass(10)
print(obj.public_method())
print(obj.value)
# print(obj.__private_method())  # This will raise an AttributeError
