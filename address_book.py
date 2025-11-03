from collections import UserDict
from datetime import date, timedelta, datetime
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
            if user.birthday is None:
                continue

            try:
                birthday_date_obj = datetime.strptime(user.birthday.value, "%d.%m.%Y").date()
            except ValueError:
                continue 

            birthday_this_year = birthday_date_obj.replace(year=today.year)

            start_of_period = today
            end_of_period = today + timedelta(days=days)

            if birthday_this_year < today:
                birthday_check = birthday_date_obj.replace(year=today.year + 1)
            else:
                birthday_check = birthday_this_year
            
            if start_of_period <= birthday_check < end_of_period:
                congratulation_date = birthday_check
                day_of_week = birthday_check.weekday() 

                if day_of_week >= 5: 

                    days_to_monday = (7 - day_of_week) + weekday 
                    congratulation_date += timedelta(days=days_to_monday)

                upcoming_birthdays.append({
                    "Name": user.name.value, 
                    "Congratulation date": congratulation_date.strftime("%d.%m.%Y")
                })
                
        return upcoming_birthdays