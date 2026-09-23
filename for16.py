N = int(input("Введите число N(>0): "))
A = float(input("Введите вещественное число A: "))
a = 1
for i in range(1, N + 1):
    a *= A
print(f"A в степени {i} = {a}")