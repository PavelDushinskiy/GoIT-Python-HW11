from collections import UserDict
import datetime

RECORDS_PER_PAGE = 30


def _now():
    return datetime.datetime.today()


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    def __repr__(self):
        return self.value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    def __init(self, ):
        pass


class Phone(Field):
    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value):
        self._value = f"Redefined: {value}"


class Birthday(Field):
    @property
    def value(self) -> datetime.datetime.date:
        return self._value

    @value.setter
    def value(self, value):
        self._value = datetime.datetime.strptime(value, "%d.%m.%Y")

    def __repr__(self):
        return datetime.datetime.strftime(self._value, "%d.%m.%Y")


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name: Name = name
        self.phones: list[Phone] = [phone] if phone is not None else []
        self.birthday = birthday

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def change_phone(self, old_phone: Phone, new_phone: Phone):
        try:
            self.phones.remove(old_phone)
            self.phones.append(new_phone)
        except ValueError:
            return f"{old_phone} does not exist"

    def delete_phone(self, phone: Phone):
        try:
            self.phones.remove(phone)
        except ValueError:
            return f"{phone} does not exist"

    def days_to_birthday(self):
        now = _now().date()
        if self.birthday is not None:
            birthday: datetime.datetime.date = self.birthday.value.date()
            m_birthday = datetime.date(year=now.year, month=birthday.month, day=birthday.day)
            if m_birthday < now:
                m_birthday = m_birthday.replace(year=now.year + 1)
                return abs(m_birthday - now).days
        return None


class AddressBook(UserDict):
    __items_per_page = 20

    def items_per_page(self, value):
        self.__items_per_page = value

    items_per_page = property(fget=None, fset=items_per_page)

    def __iter__(self):
        self.page = 0
        return self

    def __next__(self):
        records = list(self.data.items())
        start_index = self.page * self.__items_per_page
        end_index = (self.page + 1) * self.__items_per_page
        self.page += 1
        if len(records) > end_index:
            to_return = records[start_index:end_index]
        else:
            if len(records) > start_index:
                to_return = records[start_index: len(records)]
            else:
                to_return = records[:-1]
        self.page += 1
        return [{record[1]: record[0]} for record in to_return]

    def add_contact(self, name: Name, phone: Phone = None):
        contact = Record(name=name, phone=phone)
        self.data[name.value] = contact

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find_name(self, name: Name):
        try:
            return self.data[name]
        except KeyError:
            return None

    def find_phone(self, phone: Phone):
        for record in self.data.values():
            if phone in [number.value for number in record.phones]:
                return record
        return None


if __name__ == "__main__":
    addr = AddressBook()
    for x in range(RECORDS_PER_PAGE):
        addr.add_record(Record(Name(f"Name: {x}")))
    gen = iter(addr)
    print(next(gen))
