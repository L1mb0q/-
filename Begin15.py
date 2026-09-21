import math
S = float(input(" Введите площадь окружности S: "))
π = 3.14
R = math.sqrt(S / π)
L = 2 * π * R
D = 2 * R
print(f" Длина окружности L = {L}")
print(f" Диаметр окружности D = {D}")