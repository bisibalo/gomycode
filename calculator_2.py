import math

class Calculator:
    def __init__(self):
        self.operations = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y if y != 0 else float('inf')
        }

    def add_operation(self, symbol, func):
        if not callable(func):
            raise ValueError("The function must be callable.")
        self.operations[symbol] = func

    def calculate(self, num1, operation, num2):
        if operation not in self.operations:
            raise ValueError(f"Operation '{operation}' is not supported.")
        if not (isinstance(num1, (int, float)) and isinstance(num2, (int, float))):
            raise ValueError("Both inputs must be numbers.")

        try:
            return self.operations[operation](num1, num2)
        except Exception as e:
            print(f"Error during calculation: {e}")
            raise

def exponentiation(x, y):
    return x ** y

def square_root(x, _):
    if x < 0:
        raise ValueError("Cannot calculate the square root of a negative number.")
    return math.sqrt(x)

def logarithm(x, base):
    if x <= 0 or base <= 0:
        raise ValueError("Logarithm inputs must be positive.")
    return math.log(x, base)

if __name__ == "__main__":
    calc = Calculator()

    # Add advanced operations
    calc.add_operation('^', exponentiation)
    calc.add_operation('sqrt', square_root)
    calc.add_operation('log', logarithm)

    while True:
        print("\nAvailable operations: ", ', '.join(calc.operations.keys()))
        user_input = input("Enter calculation (e.g., '2 + 2') or 'exit' to quit: ").strip()

        if user_input.lower() == 'exit':
            print("Exiting calculator. Goodbye!")
            break

        try:
            parts = user_input.split()
            if len(parts) == 3:
                num1, operation, num2 = parts
                num1, num2 = float(num1), float(num2)
                result = calc.calculate(num1, operation, num2)
            elif len(parts) == 2 and parts[0].lower() == 'sqrt':
                operation, num1 = parts
                num1 = float(num1)
                result = calc.calculate(num1, operation, 0)
            elif len(parts) == 3 and parts[0].lower() == 'log':
                operation, num1, base = parts
                num1, base = float(num1), float(base)
                result = calc.calculate(num1, operation, base)
            else:
                raise ValueError("Invalid input format.")

            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")
