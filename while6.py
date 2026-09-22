N = int(input("Введите N: "))

result = 1
while N > 0:
    result = result * N 
    N = N - 2         
print(f"Двойной факториал: {result}")