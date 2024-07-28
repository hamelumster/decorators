import os
import datetime

def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            log = (
                f'{datetime.datetime.now()}:'
                f' имя функции: {old_function.__name__} вызвана с '
                f' аргументами: args: {args}, kwargs: {kwargs}\n'
            )
            with open(path, 'a') as log_file:
                log_file.write(log)

            # Создание генератора
            generator = old_function(*args, **kwargs)

            # Обертка для каждого вызова next() на генераторе
            class Generator:
                def __iter__(self):
                    return self

                def __next__(self):
                    try:
                        result = next(generator)
                        # Логирование возврата значения
                        log_ = (
                            f'{datetime.datetime.now()}: '
                            f'функция {old_function.__name__} возвращает {result}\n'
                        )
                        with open(path, 'a') as log_file:
                            log_file.write(log_)
                        return result
                    except StopIteration:
                        # Логирование завершения генератора
                        log_ = (
                            f'{datetime.datetime.now()}: '
                            f'функция {old_function.__name__} достигла StopIteration\n\n'
                        )
                        with open(path, 'a') as log_file:
                            log_file.write(log_)
                        raise

            return Generator()
        return new_function
    return __logger

# Пример использования декоратора с генератором
@logger('main.log')
def flat_generator(list_of_lists):
    for list_ in list_of_lists:
        for item in list_:
            yield item

# Тестирование генератора
if __name__ == '__main__':
    list_of_lists = [
        [1,2,3],
        [4,5,6],
        [7,8,9]
    ]
    final_list = []
    for item in flat_generator(list_of_lists):
        final_list.append(item)
    print(final_list)