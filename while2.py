A = float(input("Введите длину A: "))
B = float(input("Введите длину B: "))
count = 0
while A >= B:
    A = A - B
    count += 1
print(f"Количество отрезков B, в отрезке A {count}")
