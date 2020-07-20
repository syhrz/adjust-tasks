import random

listofnumber = [1, 2, 3 ,4, 5, 6, 7, 8, 9, 10]

i = len(listofnumber)

while (i > 0):
    r = random.randint(0, i-1)
    print(listofnumber[r])
    listofnumber.remove(listofnumber[r])
    i-=1
