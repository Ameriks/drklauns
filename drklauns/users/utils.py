import random


def generate_temp_password(length: int=8):
    if not isinstance(length, int) or length < 8:
        raise ValueError("temp password must have positive length")

    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return ''.join(map(lambda x: random.choice(chars), range(length)))
