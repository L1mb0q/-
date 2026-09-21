number = int(input("Введите двухначное число: "))
a = number // 10
b = number % 10
sum = a + b
proizved = a * b
print(f"Десятки: {a}")
print(f"Единицы: {b}")
print(f"Сумма цифр числа = {sum}")
print(f"Произведение цифр числа = {proizved}")