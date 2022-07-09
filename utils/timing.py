import time

def timing(func):
    def wrapper(*args, **kwargs):
        start = time.process_time()
        result = func(*args, **kwargs)
        end = time.process_time()
        print(func.__name__,': ', end-start, 'seconds')
        return result
    return wrapper
