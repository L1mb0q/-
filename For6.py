price = float(input("Введите цену 1 кг конфет: "))
for i in range(12, 21, 2):
    weight = i / 10.0
    print(f"{weight} кг стоит {weight * price}")