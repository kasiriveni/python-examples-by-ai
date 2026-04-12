# Lambdas

# Lambda function
square = lambda x: x ** 2
print("Square of 5:", square(5))

# Lambda with map
numbers = [1, 2, 3, 4]
squared_numbers = list(map(lambda x: x ** 2, numbers))
print("Squared Numbers:", squared_numbers)
