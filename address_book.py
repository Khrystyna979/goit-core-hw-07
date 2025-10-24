from collections import UserDict
from datetime import date, timedelta
from record import Record

class AddressBook(UserDict):
    """
    Class that allow to create address book with all records
    """
    def add_record(self, record: Record):
        key = record.name.value
        self.data[key] = record

    def find(self, name: str):
        return self.data.get(name, None)
    
    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    def __str__(self):
        if not self.data:
            return 'Address book is empty'
        else:
            records_str = '\n'.join(str(record) for record in self.data.values())
            return records_str
        
    def get_upcoming_birthdays(self, days=7, weekday=0):
        upcoming_birthdays = []
        today = date.today()

        for user in self.data.values():

            birthday_this_year = user.birthday.value.replace(year=today.year)

            if birthday_this_year < today:
                birthday_next_year = user.birthday.value.replace(year=today.year + 1)

            if 0 <= (birthday_this_year - today).days <= days: 

                if birthday_this_year.weekday() >= 5:
                    days_ahead = weekday - birthday_this_year.weekday()
                    
                    if days_ahead <= 0:
                        days_ahead += 7
                        birthday_this_year += timedelta(days=days_ahead)
                        upcoming_birthdays.append({
                            "Name": user.name.value, 
                            "Congratulation date": birthday_this_year.strftime("%Y.%m.%d")
                            })
            
            elif (birthday_next_year - today).days in range(0, 8):

                if birthday_next_year.weekday() >= 5:
                    days_ahead = weekday - birthday_next_year.weekday()

                    if days_ahead <= 0:
                        days_ahead += 7
                        birthday_next_year += timedelta(days=days_ahead)
                        upcoming_birthdays.append({
                            "Name": user.name.value, 
                            "Congratulation date": birthday_next_year.strftime("%Y.%m.%d")
                            })
            
        return upcoming_birthdays


