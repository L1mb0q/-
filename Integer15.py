number = int(input("Введите трехзначное число: "))
a = number // 100 # Сотни
b = (number // 10) % 10 #Десятки
c = number % 10 # Единицы
result = b * 100 + a * 10 + c 
print(f"Результат = {result}")