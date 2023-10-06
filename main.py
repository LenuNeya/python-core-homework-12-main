'''
Консольний бот-помічник, який розпізнає команди, що вводяться з клавіатури, і відповідає відповідно до введеної команди
'''


from decorator_error import input_error
from parameters_processing import sanitize_phone_number, check_name, user_input_split
from classes import AddressBook, Name, Phone, Record, Birthday


CONTACTS = AddressBook()


@input_error
def add_or_change(name: str, phone: str, add=True) -> str:
    '''
    Обробка команд add і change
    add - додає користувача і номер телефона в словник;
    change - змінює номер телефона для вказаного користувача
    '''
    clean_phone = sanitize_phone_number(phone)
    if len(clean_phone) != 12:
        raise ValueError('The phone number format is incorrect')
    elif not name:
        raise ValueError('Enter user name')

    if add:
        if CONTACTS.find(name) is not None:
            raise ValueError('User with that name already exists')
        msg = f'Nice to meet you {name}!'
    else:
        if CONTACTS.find(name) is None:
            raise ValueError(f'User {name} not found')
        msg = f'Saved your new phone number {clean_phone}!'

    CONTACTS.add_record(Record(name=name, phone=clean_phone))

    return msg


@input_error
def add_birthday(name: str, birthday: str) -> str:
    '''
    Додаємо день надодження для контакту.
    '''
    contact = CONTACTS.find(name)
    if contact is None:
        raise ValueError(f'User {name} not found')
    
    contact.add_birthday(birthday)

    msg = f'Saved your birthday {birthday}!'
    return msg


@input_error
def verification_name(name: str) -> str:
    '''
    Перевіряємо корректність введеного імені користувача.
    І`мя не може починатись з цифри та має містити лише латинські літери, цифри, або символ _ 
    '''
    correct_name = check_name(name)
    if correct_name is None:
        raise ValueError('Name must start with a Latin letter or the symbol "_" and contain only Latin letters and numbers, or the symbol "_"')
    else:
        return correct_name.group()


def fin_work() -> str:
    '''
    Обробка команди завершення роботи бота
    '''
    CONTACTS.save_data()
    return f'Good bye!'


@input_error
def get_phone(name: str) -> str:
    '''
    Обробка команди phone
    phone - повертає номер телефона за іменем вказаного користувача
    '''
    if not name:
        raise ValueError('Please enter user name')
    elif CONTACTS.find(name) is None:
        raise ValueError (f'User {name} not found')

    contact = CONTACTS.find(name)
    phone_nuumbers = '; '.join(p.value for p in contact.phones)
    return f'Your phones number {phone_nuumbers}'


@input_error
def add_phone(name: str, phone: str) -> str:
    '''
    Обробка команди add_phone
    add_phone - додає номер телефона за іменем вказаного користувача
    '''
    if not name or not phone:
        raise ValueError('Please enter user name')
    elif CONTACTS.find(name) is None:
        raise ValueError (f'User {name} not found')

    contact = CONTACTS.find(name)
    contact.add_phone(phone)

    phone_nuumbers = '; '.join(p.value for p in contact.phones)
    return f'Your phones number {phone_nuumbers}'


def search(text: str) -> str:
    '''
    Обробка команди пошуку записів за частиної імені, або номера телефона
    '''
    return CONTACTS.search(text)


def hello() -> str:
    '''
    Обробка команди початку роботи бота
    '''
    return 'How can I help you?'


@input_error
def show_all() -> str:
    '''
    Обробка команди show_all
    show_all - виводить на екран усі записи книги
    '''
    if len(CONTACTS.data) == 0:
        raise ValueError('Users base is empty')

    iterator = CONTACTS.iterator()
    answer_text = ''
    for page in iterator:
        answer_text = f'{answer_text}{page}\n'

    return answer_text


'''
Словник для зберігання відповідності команд та функцій для їх обробки
'''
COMMANDS = {
    'hello': {'func': hello, 'param': 0},
    'add': {'func': add_or_change, 'param': 2, 'ex_p': True}, 
    'change': {'func': add_or_change, 'param': 2, 'ex_p': True},
    'phone': {'func': get_phone, 'param': 1},
    'add_phone': {'func': add_phone, 'param': 2},
    'add_birthday': {'func': add_birthday, 'param': 2},
    'show_all': {'func': show_all, 'param': 0},
    'search': {'func': search, 'param': 1},
    'exit': {'func': fin_work, 'param': 0}
}


@input_error
def parser_user_input(user_input: str):
    '''
    Обробка даних, введених користувачем
    '''
    params_input = user_input_split(user_input)
    if not params_input:
        raise ValueError(hello())

    command = params_input[0]
    dict_finction = COMMANDS.get(command, None)
    if dict_finction is None:
        raise ValueError(hello())
    
    count_arg = dict_finction['param']
    args = params_input[1:]
    if len(args) < count_arg and count_arg == 2:
        raise ValueError('Give me name and phone please.')
    elif len(args) < count_arg and count_arg == 1:
        raise ValueError('Enter user name please.')

    active_finction = dict_finction['func']
    ex_p = dict_finction.get('ex_p')
    if count_arg == 2:
        p1, p2 = args[:2]
        if ex_p:
            return active_finction(p1.title(), p2, (command=='add'))
        else:
            return active_finction(p1.title(), p2)
    elif count_arg == 1:
        return active_finction(args[0].title())
    else:
        return active_finction()


def main():
    '''
    Головна функція роботи бота
    '''
    try:
        CONTACTS.load_data()
    except:
        CONTACTS.open_empty_json()
    
    bot_answer = 'Hi here!'
    
    while True:
        
        user_input = input(f'{bot_answer} --> ')
        
        bot_answer = parser_user_input(user_input)
        print(bot_answer)
        
        if bot_answer == 'Good bye!':
            break
        else:
            bot_answer = ''


if __name__ == '__main__':
    main()