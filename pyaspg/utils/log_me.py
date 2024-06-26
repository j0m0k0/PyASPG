import logging
from functools import wraps
from datetime import datetime

# Get the current date and time to create a log file name
current_time = datetime.now().strftime('%m-%d-%Y-%H%M%S')
log_filename = f'logs/{current_time}.log'

# Configure logging to write to a file without printing to standard output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler(log_filename)
])

def log_me(cls):
    # Iterate through all the attributes of the class
    for attr_name, attr_value in cls.__dict__.items():
        # Check if the attribute is a callable (method)
        if callable(attr_value):
            # Replace the method with a wrapped version
            setattr(cls, attr_name, log_decorator(attr_value, cls.__name__))
    return cls

def log_decorator(func, class_name):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Log method entry with arguments
        logging.info(f"Entering {class_name}.{func.__name__} with args: {args[1:]} and kwargs: {kwargs}")
        
        # Execute the function
        result = func(*args, **kwargs)
        
        # Log method exit with result
        logging.info(f"Exiting {class_name}.{func.__name__} with result: {result}\n")
        
        return result
    return wrapper
