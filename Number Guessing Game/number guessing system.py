import random 
random_number=random.randint(1,100)
while True:
    num=int(input("Guess a number between 1 and 100: "))
    if num>random_number:
        print("guess lower")
    elif num<random_number:
        print ("guess higher")
    else:
        print("Congratulations you guessed the number")
        break
    