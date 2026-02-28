from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not (isinstance(new_value, str) and new_value.isdigit() and len(new_value) == 10):
            raise ValueError("Phone number must contain exactly 10 digits.")
        self._value = new_value


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)
        if phone_obj is None:
            raise ValueError("Phone number not found.")
        self.phones.remove(phone_obj)

    def edit_phone(self, old_phone, new_phone):
        phone_obj = self.find_phone(old_phone)
        if phone_obj is None:
            raise ValueError("Phone number not found.")
        phone_obj.value = new_phone

    def find_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]


def input_validator(argLength, errorMessage):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if len(args) > 0 and len(args[0]) != argLength:
                return errorMessage
            try:
                return func(*args, **kwargs)
            except ValueError:
                return "Error: Invalid command."
        return wrapper
    return decorator

def parse_input(user_input: str) -> tuple:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_validator(2, "Invalid command. Use 'add <name> <phone>'.")
def add_contact(args: list, contacts: dict) -> str:
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_validator(2, "Invalid command. Use 'change <name> <phone>'.")    
def change_contact(args: list, contacts: dict) -> str:
    name, phone = args

    if name not in contacts:
        return "Contact not found."

    contacts[name] = phone
    return "Contact updated."

@input_validator(1, "Invalid command. Use 'phone <name>'.")
def show_phone(args: list, contacts: dict) -> str:
    (name,) = args

    if name not in contacts:
        return "Contact not found."

    return contacts[name]


def show_all(contacts: dict) -> str:
    if not contacts:
        return "No contacts saved."

    lines = [f"{name}: {phone}" for name, phone in contacts.items()]
    return "\n".join(lines)


def exit_program():
    print("Good bye!")
    exit(0)

def main():
    contacts = {}
    print("Welcome to the assistant bot!")

    try:
        while True:
            user_input = input("Enter a command: ").strip()

            if not user_input:
                continue

            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                exit_program() # break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                print(add_contact(args, contacts))
            elif command == "change":
                print(change_contact(args, contacts))
            elif command == "phone":
                print(show_phone(args, contacts))
            elif command == "all":
                print(show_all(contacts))
            else:
                print("Invalid command.")
    except KeyboardInterrupt:
        exit_program()


if __name__ == "__main__":
    main()
