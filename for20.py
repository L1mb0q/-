N = int(input("Введите N (>0): "))
sum = 0
current = 1
for i in range(1, N + 1):
    current *= i 
    sum += current
print(f"Сумма факториалов: {sum}")