number = int(input("Введите трехзначное число: "))
a = number % 10
b = number // 10  % 10
print(f"Единицы: {a}")
print(f"Десятки: {b}")