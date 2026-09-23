N = int(input("Введите число N(>0): "))
A = float(input("Введите вещественное число A: "))
sum = 1
current = 1
for _ in range(N):
    current *= A
    sum += current
print(f"Сумма = {sum}")