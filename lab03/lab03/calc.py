def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

# Пример работы функций
# Намеренная ошибка для демонстрации revert
result = 10 / 0

def safe_divide(a, b):
    if b == 0:
        return "Ошибка: деление на ноль!"
    return a / bif __name__ == "__main__":
    x = 10
    y = 5
    print(f"Сложение: {x} + {y} = {add(x, y)}")
    print(f"Вычитание: {x} - {y} = {subtract(x, y)}")
    print(f"Умножение: {x} * {y} = {multiply(x, y)}")
