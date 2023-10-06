from collections import UserDict
from datetime import datetime, date
import json




class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value
    
    def __repr__(self) -> str:
        return f'{self.value}'
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Name(Field):
    pass


class Phone(Field):
    
    def __str__(self):
        return str(self.value)
    
    def __init__(self, value: str):
        super().__init__(value)
        self.validate_phone(value)

    def validate_phone(self, phone):
        if not (len(phone) == 12 and phone.isdigit()):
            raise ValueError("Phone number is not valid")


class Birthday(Field):
    def __init__(self, value: str):
        super().__init__(value)
        self.validate_birthday(value)

    def validate_birthday(self, birthday):
        try:
            self.value = datetime.strptime(birthday, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid birthday format (should be 'DD.MM.YYYY')")
    
    def __str__(self):
        birthday_value = "01.01.0001"
        if self.value:
            birthday_value = self.value.strftime("%d.%m.%Y")
        return f'{birthday_value}'
    


class Record:
    
    def __init__(self, name, phone='', birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        if phone:
            self.phones.append(Phone(phone))
        if birthday:
            self.birthday = Birthday(birthday)
        
    
    def __str__(self):
        birthday_value = "-"
        if self.birthday:
            birthday_value = self.birthday.value.strftime("%d.%m.%Y")
        
        return 'Contact: {:<10} | {:^10} | {:<5}'.format(self.name.value, birthday_value, '; '.join(p.value for p in self.phones))
    
    
    def add_phone(self, phone: str):
        if phone not in [p.value for p in self.phones]:
            self.phones.append(Phone(phone))
    

    def remove_phone(self, phone: str):
        for i in self.phones:
            if i.value == phone:
                self.phones.remove(i)
                break    
    
    def edit_phone(self, old_phone, new_phone):
        phone = None
        for i in self.phones:
            if i.value == old_phone:
                phone = i
                break
        if phone is None:
            raise ValueError("Phone number is not fided")
        else:
            phone.value = new_phone

    def find_phone(self, phone: str):
        for i in self.phones:
            if i.value == phone:
                return i
        return None
    
    def days_to_birthday(self):
        if self.birthday is None:
            return None
        
        today = date.today()
        next_birthday = self.birthday.value.replace(year=today.year)
        if next_birthday < today:
            next_birthday = self.birthday.value.replace(year=(today.year + 1))
            
        delta = next_birthday - today
        return delta.days
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)


      

class AddressBook(UserDict):
    
    def __init__(self, filename="addressbook.json"):
        super().__init__()
        self.contacts_on_page = 5
        self.count_pages = 0
        self.n_page = 1
        self.idx = 0
        self.data_list = []
        self.filename = filename

    
    def __iter__(self):
        return self
    

    def __next__(self):
        
        if self.n_page <= self.count_pages:
            page_list = []
            data_slice = self.data_list[self.idx:self.contacts_on_page*self.n_page]
            result = ''
            for key, record in data_slice:
                if data_slice.index((key, record)) == (len(data_slice) - 1):
                    self.n_page += 1
                page_list.append(record)
                self.idx += 1
            
            result = '\n'.join(str(p) for p in page_list)   
            return f'Page #{self.n_page - 1}\n{result}'
        
        raise StopIteration
    

    def add_record(self, record: Record):
        Key = record.name.value
        self.data.update({Key:record})
    

    def find(self, name):
        if name in self.data:
            return self.data[name]


    def delete(self, name):
        if name in self.data:
            del self.data[name]
    

    def iterator(self, contacts_on_page=5):
        try:
            self.contacts_on_page = int(contacts_on_page)
        except ValueError:
            raise ValueError("contacts_on_page must be int")
        
        count_pages = len(self.data)/self.contacts_on_page
        pages = int(count_pages)
        if count_pages > pages or pages == 0:
            self.count_pages = pages + 1
        else:
            self.count_pages = pages
        
        self.data_list = [record for record in self.data.items()]
        self.idx = 0
        self.n_page = 1
        return self
    

    def open_empty_json(self):
        print("Start open_empty_json function")
        with open(self.filename, 'w', encoding='utf-8') as fb:
            json.dump({}, fb)
    
    
    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as fb:
            data = {str(name): {
                'phones': [str(phone) for phone in record.phones],
                'birthday': str(record.birthday) if record.birthday else None
            } for name, record in self.data.items()}
            json.dump(data, fb)


    def load_data(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as fb:
                try:
                    data = json.load(fb)
                except:
                    return None
                for key, value in data.items():
                    n_record = Record(name=key, birthday=value.get('birthday', None))
                    for phone in value.get('phones'):
                        n_record.add_phone(phone)
                    self.add_record(n_record)
        except FileNotFoundError:
            with open(self.filename, 'w') as fb:
                json.dump({}, fb)
    

    def search(self, search_text):
        results = []
        for name, record in self.data.items():
            if search_text.lower() in name.lower():
                results.append(record)
                continue
            for phone in record.phones:
                if search_text.isdigit() and search_text in phone.value:
                    results.append(record)
                    continue
        
        if results:
            result = '\n'.join(str(p) for p in results)   
            return f'Results:\n{result}'
            
        return f'No results "{search_text}"'
    



if __name__ == '__main__':
    
    # Створення нової адресної книги
    book = AddressBook()

    # book.add_record(Record(name='Vitalii', phone='380000000000', birthday='12.05.1990'))
    # book.add_record(Record(name='Tom', phone='381111111111', birthday='03.02.1977'))
    # book.add_record(Record(name='Jane', phone='389876543210', birthday='30.06.2000'))
    # book.add_record(Record(name='Jane2', phone='382222222222', birthday='06.01.1986'))
    # book.add_record(Record(name='John2', phone='383333333333'))
    # book.add_record(Record(name='Andry', phone='384444444444', birthday='17.09.1980'))
    # book.add_record(Record(name='Lisa', phone='385555555555', birthday='04.07.1975'))
    # book.add_record(Record(name='Natasha', phone='386666666666', birthday='01.11.1991'))
    # book.add_record(Record(name='Ira', phone='387777777777', birthday='09.10.1993'))
    # book.add_record(Record(name='Vasya', phone='388888888888', birthday='09.05.1965'))
    # book.add_record(Record(name='Ivan', phone='389999999999', birthday='21.04.1968'))
    # book.add_record(Record(name='Stas', phone='380123456789', birthday='29.03.1974'))
    # book.add_record(Record(name='Sasha', phone='389876543210'))
    # book.add_record(Record(name='Marina', phone='381234567890', birthday='30.06.1976'))
    # book.add_record(Record(name='Boston', phone='380987654321', birthday='10.09.1993'))
    # book.add_record(Record(name='Vadim', phone='238345678901', birthday='12.10.1989'))
    # book.add_record(Record(name='Oleg', phone='138098765432', birthday='13.01.1978'))
    # book.add_record(Record(name='Valera', phone='383456789012', birthday='10.02.1974'))
    # book.add_record(Record(name='Anya', phone='238109876543', birthday='15.08.1991'))
    # book.add_record(Record(name='Kolya', phone='438567890123', birthday='16.03.1993'))
    # book.add_record(Record(name='Misha', phone='338210987654', birthday='08.01.1990'))

    # # Створення запису для John
    # john_record = Record("John",birthday='06.10.2000')
    # # john_record.add_phone("12345abcde")
    # john_record.add_phone("385555555555")
    # john_record.add_phone("381234567890")

    # # Додавання запису John до адресної книги
    # book.add_record(john_record)

    
    
    # # print(john_record.birthday)
    
    # book.save_data()
    book.load_data()

    # iterator = book.iterator()
    # for page in iterator:
    #     print(page)

    # print(book.search('ol'))

    print(book.search('222'))

    

    








