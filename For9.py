a = int(input("Введите A: "))
b = int(input("Введите B: "))

total_sum = 0
for i in range(a, b + 1):
    total_sum += i ** 2
print("Сумма квадратов:", total_sum)