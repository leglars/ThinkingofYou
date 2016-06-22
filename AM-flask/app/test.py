from threading import Thread
from time import sleep


def sleepy():
    sleep(5)
    print("i wake up")


def testing():
    if True:
        test = Thread(target=sleepy)
        test.start()

    print("out of if")
    return "maybe different"


print(testing())