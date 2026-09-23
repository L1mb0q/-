N = int(input("Введите число N (>0): "))
sum = 0
for i in range(1, N + 1):
    odd_number = 2 * i - 1
    sum += odd_number
print(f"Квадрат числа {i} = {sum}")