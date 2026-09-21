a = int(input("Введите a: "))
b = int(input("Введите b: "))
total_sum = 0
for i in range(a, b + 1):
    total_sum += i 
print(f"Сумма: {total_sum}")