from address_book import AddressBook, Record
from colorama import Fore, Style
from record import PhoneValidationError

commands = f"""
{Fore.YELLOW}hello{Style.RESET_ALL} - how can I help you
{Fore.YELLOW}add{Fore.GREEN} [name] [phone]{Style.RESET_ALL} - add new contact with name and phone or add phone to existing name
{Fore.YELLOW}change{Fore.GREEN} [name] [old phone] [new phone]{Style.RESET_ALL} - change contact's old phone with new phone 
{Fore.YELLOW}phone{Fore.GREEN} [name]{Style.RESET_ALL} - show phones of contact
{Fore.YELLOW}delete{Fore.GREEN} [name]{Style.RESET_ALL} - delete contact
{Fore.YELLOW}add-birthday{Fore.GREEN} [name] [date of birth]{Style.RESET_ALL} - add birthday to contact
{Fore.YELLOW}show-birthday{Fore.GREEN} [name]{Style.RESET_ALL} - show birthday of contact
{Fore.YELLOW}birthdays{Style.RESET_ALL} - show birthdays for the next 7 days with the dates when they should be congratulated.
{Fore.YELLOW}all{Style.RESET_ALL} - show all names and their phones
{Fore.YELLOW}close or exit{Style.RESET_ALL} - bot shutdown
"""
def input_error(func):
    """
    Function for error handling
    """
    def inner(*args, **kwargs):

        try:
            return func(*args, **kwargs)
        except PhoneValidationError:
            return 'Phone number must have exactly 10 digits.'
        except ValueError:
            return "Please enter valid contact data."
        except KeyError:
            return 'Contact with this name not found.'
        except IndexError:
            return 'Please provide all required information.'
        except AttributeError:
            return 'Contact not found.'

    return inner

@input_error
def parse_input(user_input: str):
    """
    Function for pursing user input
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    """
    Function for adding contact in book
    """
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact_phone(args, book: AddressBook):
    """
    Function for changing contact phone
    """
    name, old_phone, new_phone, *_ = args
    record = book.find(name)

    if old_phone and new_phone:
        record.edit_phone(old_phone, new_phone)

    return "Phone updated."
    
@input_error    
def show_phone(args, book: AddressBook):
    """
    Function that shows phone of current name
    """
    name, *_ = args
    record = book.find(name)
    
    return record.show_phone_by_name()
    
@input_error
def delete(args, book: AddressBook):
    """
    Function that delete contact from book
    """
    name, *_ = args
    record = book.find(name)

    book.delete(name)
    return 'Contact deleted'

@input_error      
def show_all(book: AddressBook):
    """
    Function that shows all the names and phones
    """
    return book

@input_error
def add_birthday(args, book: AddressBook):
    """
    Function that add contact's birthday 
    """
    name, date_of_birth, *_ = args
    record = book.find(name)

    record.add_birthday(date_of_birth)

    return 'Birthday added.'

@input_error
def show_birthday(args, book: AddressBook):
    """
    Function that show contact's birthday 
    """
    name, *_ = args
    record = book.find(name)

    return record.show_birthday()

@input_error
def birthdays(book: AddressBook):
    """
    Function that show birthdays for the next 7 days with the dates when they should be congratulated
    """
    birthdays_list = book.get_upcoming_birthdays()
    
    if not birthdays_list:
        return 'There is no upcoming birthdays'
    
    return birthdays_list

def main():
    """
    function that performs the main processing
    """
    book = AddressBook()
    print("Welcome to the assistant bot!", 'Commands: ', commands, sep='\n')

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == 'change':
            print(change_contact_phone(args, book))
        elif command == 'phone':
            print(show_phone(args, book))
        elif command == 'delete':
            print(delete(args, book))
        elif command == 'add-birthday':
            print(add_birthday(args, book))
        elif command == 'show-birthday':
            print(show_birthday(args, book))
        elif command == 'birthdays':
            print(birthdays(book))
        elif command == 'all':
            print(show_all(book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
    