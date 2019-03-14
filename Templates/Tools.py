import random


def create_url(len=25):
    url = ""
    for i in range(len):
        url += random.choice(alphabet)
    return url


alphabet = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
for i in range(ord("a"), ord("z") + 1):
    alphabet.append(chr(i))
    alphabet.append(chr(i).upper())
