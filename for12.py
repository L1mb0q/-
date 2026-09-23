N = int(input("Введите число N (>0): "))
proizvedenie = 1
current = 1.1
for _ in range(N):
    proizvedenie *= current 
    current += 0.1
print(f"Произведение {proizvedenie}")