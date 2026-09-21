import math
a = float(input(" Введите катет a: "))
b = float(input(" Введите катет b: "))
c = math.sqrt(a ** 2 + b ** 2)
P = a + b + c
print(f" Гипотенуза = {c}")
print(f" Периметр = {P}")