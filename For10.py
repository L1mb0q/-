n = int(input("Введите N: "))
total_sum = 0.0
for i in range(1, n + 1):
    total_sum += 1 / i
print("Сумма:", total_sum)