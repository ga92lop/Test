import time

def Fibonacci(n):
    if n == 1 or n == 2:
        return 1
    else:
        return Fibonacci(n-1) + Fibonacci(n-2)


t1 = time.time()
print(Fibonacci(36))
t2 = time.time()
print("it takes", t2-t1, "s using method 1")



def New_methad(n):
    num = list()
    num.append(1)
    num.append(1)
    if n == 1 or n == 2:
        return 1
    for i in range(n-2):
        temp = num[0] + num[1]
        num[0] = num[1]
        num[1] = temp
    return num[1]


t1 = time.time()
print(New_methad(36))
t2 = time.time()
print("it takes", t2-t1, "s using method 2")
