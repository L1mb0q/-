n = int(input("Введите число n (n > 0): "))
k = 0
while n > 1:
    n = n // 2
    k += 1 
    print(f"Показатель степени k: {k}")