number = int(input("Введите трехзначное число: "))
a = (number // 10) % 10
b = number % 10
c = number // 100
result = b * 100 + a * 10 + c
print(result)