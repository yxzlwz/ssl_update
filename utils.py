import random


def random_str(length: int = 4) -> str:
    return ''.join(
        random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=length))
