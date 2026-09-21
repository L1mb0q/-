A = int(input("Введите A (A < B): "))
B = int(input("Введите B (B > A): "))
count = 0
for i in range(A, B + 1):
    print(i)
    count += 1
print("Количество:", count)