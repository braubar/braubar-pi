from matplotlib import pyplot


f = open("/tmp/braubar.temp", 'rb')
a = f.readlines()
b = []
for i in range(len(a)):
    try:
        a[i] = float(a[i])
        if a[i] > 120.0:
            print("if", a[i])
            a[i] = 120.0
    except ValueError:
        a[i] = 120.0
        print("exept", a[i])
    except TypeError:
        a[i] = 120.0
        print("exept", a[i])
print(a)
pyplot.plot(a)
pyplot.show()
