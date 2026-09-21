number = int(input("Введите трехзначное число: "))
a = number % 100 
b = number // 100 #Сотни
result = a * 10 + b 
print(result)