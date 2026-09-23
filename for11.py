N = int(input("Введите число N (>0): "))
sum = 0
for i in range(N, 2 * N + 1):
    sum += i ** 2 
print(f"Сумма = {sum}")