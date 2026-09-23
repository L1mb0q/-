N = int(input("Введите N (>0): "))
factorial = 1
for i in range(1, N + 1):
    factorial *= i
print(f"{N}! = {factorial}")