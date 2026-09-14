import math


def minimum_code_length(alphabet_size: int, num_messages: int) -> int:
    return math.ceil(math.log(num_messages, alphabet_size))


def num_possible_codes(alphabet_size: int, length: int) -> int:
    return alphabet_size ** length
