import math
x1 = float(input("Введите вершину x1: "))
y1 = float(input("Введите вершину y1: "))
x2 = float(input("Введите вершину x2: "))
y2 = float(input("Введите вершину y2: "))
distance = math.sqrt((x2 - x1)**2) + ((y2 - y1)**2)
print(f"Расстояние = {distance}")