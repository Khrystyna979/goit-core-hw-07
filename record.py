from datetime import datetime

class Field:
    
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value: str):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value: str):
        super().__init__(value)
        if not (len(self.value) == 10 and self.value.isdigit()):
            raise PhoneValidationError('Phone should have 10 numbers')
        
class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        try:
            datetime.strptime(value, '%d.%m.%Y').date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
             
class Record:
    """
    Class that creates record (name, phones, birthday) for object
    """
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        return self.phones.append(Phone(phone))
    
    def show_phone_by_name(self):
        return f'Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}'
        
    def find_phone(self, phone: str) -> str:
        for existing_phone in self.phones:
            if existing_phone.value == phone:
                return existing_phone
        return None
            
    def remove_phone(self, phone: str):
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
            return True
        else:
            raise ValueError('Phone not found')
            
    def edit_phone(self, phone: str, new_phone: str):
        if self.find_phone(phone):
            self.add_phone(new_phone)
            self.remove_phone(phone)
        else:
            raise ValueError('The input data is incorrect.')
        
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday) 
        
        return self.birthday

    def show_birthday(self):
        return f'Contact name: {self.name.value}, birthday: {self.birthday}'

    def __str__(self):
        if self.birthday:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class PhoneValidationError(ValueError):
    pass
