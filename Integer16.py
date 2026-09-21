number = int(input("Введите трехзначное число: "))
a = number // 100 # Сотни
b = (number // 10) % 10 #Десятки
c = number % 10 # Единицы
result = a * 100 + c * 10 + b
print(f"Результат = {result}")