a=1

def test():
    global a
    a+=1

def test2():
    a=3
    print(a)




test()
print(a)

test2()
print(a)