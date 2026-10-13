# calc.py
 - версия 2: сложение и вычитание
a = float(input("Введите первое число: "))
b = float(input("Введите второе число: "))
op = input("Введите операцию (+ или -): ")

if op == '+':
    result = a + b
    print(f"Результат сложения: {result}")
elif op == '-':
    result = a - b
    print(f"Результат вычитания: {result}")
else:
    print("Неизвестная операция")
