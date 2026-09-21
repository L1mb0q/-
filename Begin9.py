import math
a = float(input("Введите число a: "))
b = float(input("Введите число b: "))
if a >= 0 and b >= 0:
    geo_mean = math.sqrt(a * b)
    print(f"Среднее геометрическое = {geo_mean}")
else:
    print("Числа должны быть неотрицательными!")