number = int(input("Введите трехзначное число: "))
a = number % 10
b = number // 10
result = a * 100 + b
print(result)