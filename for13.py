N = int(input("Введите число N (>0): "))
sum = 0
current = 1.1
sign = 1
for _ in range(N):
    sum += sign * current
    sign = -sign
    current += 0.1
print(f"Значение выражения = {sum}")