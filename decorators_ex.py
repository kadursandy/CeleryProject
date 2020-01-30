def logger(orig_func):
    import logging
    logging.basicConfig(filename=f'{orig_func.__name__}.log', level=logging.INFO)

    def wrapper(*args, **kwargs):
        print('Executed first')
        logging.info(f'args {args} kwargs {kwargs}')
        return orig_func(*args, **kwargs)

    return wrapper


def display_second(orig_fuc):
    def wrapper(*args, **kwargs):
        print('Executed second')
        return orig_fuc(*args, **kwargs)

    return wrapper


def executed_time(outer_func):
    import time
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = outer_func(*args, **kwargs)
        t2 = time.time() - t1
        print(f'{outer_func.__name__} ran in {t2} secs')
    return wrapper


@display_second
@logger
@executed_time
def display(msg):
    print(f'Sent message {msg}')
    return 1

# display = display_second(logger(display()))
if __name__ == '__main__':
    print(display('Hello World!!'))
