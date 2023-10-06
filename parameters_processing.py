from re import search, sub


def format_phone_number(func):

    def decorate(phone):
        
        clear_phone = func(phone)
        
        pattern = r'^(0|380)\d+'
        correct_phone = search(pattern, clear_phone)
        if correct_phone is None:
            return ''
        else:
            clear_phone = correct_phone.group()

        if clear_phone[0] == '0':
            return f'38{clear_phone}'
        elif clear_phone[0] == '3':
            return f'{clear_phone}'

    return decorate 
    

@format_phone_number
def sanitize_phone_number(phone: str) -> str:
    new_phone = (
        phone.strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
    )

    return (new_phone if new_phone.isdigit() else '') 


def check_name(name: str) -> str:
    
    pattern = r'^[a-zA-Z_]+\w+'
    correct_name = search(pattern, name)
    if correct_name is not None:
        return correct_name.group()


def user_input_split(user_input: str) -> list:

    user_input = user_input.strip().lower()
    user_input = sub(r'(good bye|close|stop)', 'exit', user_input)
    user_input = sub(r'show all', 'show_all', user_input)

    return user_input.split(" ")
    
