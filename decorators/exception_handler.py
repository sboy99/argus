import functools

from lib import Logger

def ExceptionHandler(on_exception=None):
    """
    A decorator to handle exceptions in a function.
    
    :param on_exception: Optional callback function to handle the exception.
                         If provided, it will be called with the exception.
    """
    logger = Logger('ExceptionHandler')

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if on_exception:
                    on_exception(e)
                else:
                    logger.error(f"Something went wrong in {func.__name__}: {e}")
                return None
        return wrapper
    return decorator
