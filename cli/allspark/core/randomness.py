import string
import random

default_word_list = {
    "colour": ["red", "green", "blue", "black", "yellow", "pink", "neon", "white", "purple", "spotted", "stripey"],
    "transformer": ["optimusPrime", "bumblebee", "ironHide", "jazz", "ratchet", "sideswipe", "jolt", "skids"]
}

def username(type_a="colour", type_b="transformer", word_list=default_word_list, min_num=0, max_num=9999):
    num = str(random.randint(min_num, max_num))
    return random.choice(word_list["colour"]) + random.choice(word_list["transformer"]) + num

def password(length=32, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(length))
