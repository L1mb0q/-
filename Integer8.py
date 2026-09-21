number = int(input("Введите двухначное число: "))
a = number // 10
b = number % 10
number1 = b * 10 + a
print(f"Число после перестановки: {number1}")