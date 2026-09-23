N = int(input("Введите число N(>0): "))
A = float(input("Введите вещественное число A: "))
sum = 1.0 
current = 1.0
sign = -1
for _ in range(N):
    current *= A
    sum += sign * current
    sign = -sign
print(f"Значение выражения: {sum}")