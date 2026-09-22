A = float(input("Введите длину A: "))
B = float(input("Введите длину B: "))
while A >= B:
    A = A - B
print(f"Длина незанятой части отрезка A: {A}")