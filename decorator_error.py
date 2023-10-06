def input_error(func):
    ''' 
    Декоратор для обробки команд
    :param func: Функція для декорування.
    :return: функція - декоратор.
    '''
    def print_error(*args):
        try:
            bot_answer = func(*args)
        except ValueError as msg_error:
            bot_answer = msg_error.args[0]
        
        return bot_answer

    return print_error
