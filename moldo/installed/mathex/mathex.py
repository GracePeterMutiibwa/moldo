def modulo(dividend, divisor):
    return float(dividend) % float(divisor)

def clamp(value, min_val, max_val):
    return max(float(min_val), min(float(max_val), float(value)))

def is_even(value):
    return int(float(value)) % 2 == 0

def average(a, b):
    return (float(a) + float(b)) / 2
