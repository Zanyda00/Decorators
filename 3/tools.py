from datetime import datetime


def logger(path):
    def __logger(old_function):
        log = {}

        def new_function(*args, **kwargs):
            date = datetime.now().date()
            time = datetime.now().time()
            result = old_function(*args, **kwargs)
            log.update({
                'date': date,
                'time': time,
                'name': old_function.__name__,
                'arguments': f'{args}, {kwargs}',
                'result': result
            })
            with open(f'{path}', 'a') as f:
                for key, value in log.items():
                    f.write(f'{key}: {value}\n')
                f.write('\n')
            return result

        return new_function

    return __logger
