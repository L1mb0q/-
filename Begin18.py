A = float(input("Введите координату A: "))
B = float(input("Введите координату B: "))
C = float(input("Введите координату C (находится между A и B): "))
AC = C - A
BC = B - C
print(f"Отрезок AC = {AC}")
print(f"Отрезок BC = {BC}")
print(f"Произведение отрезков AC и BC = {BC * AC}")