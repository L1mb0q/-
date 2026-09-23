N = int(input("Введите число N(>0): "))
A = float(input("Введите вещественное число A: "))
result = 1
for _ in range(N):
    result *= A
print(f"{A} в степени {N} = {result}")