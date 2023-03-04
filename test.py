def greet(name):
    def say_hi():
        return f'Hi {name}!'
    return say_hi

message = greet('John')

# def greet():
#     name = "John"
#     return lambda: "Hi " + name

# message = greet()

# print(message())

