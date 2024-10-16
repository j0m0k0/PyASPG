import random

def generate_random_error(error_rate):
    if not 0 <= error_rate <= 1:
        raise ValueError("error_rate must be between 0 and 1 inclusive.")
    
    return random.uniform(-error_rate, error_rate)
