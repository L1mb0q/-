a = int(input("Введите A: "))
b = int(input("Введите B: "))

total_sum = 1
for i in range(a, b + 1):
    total_sum *= i
print("Произведение:", total_sum)