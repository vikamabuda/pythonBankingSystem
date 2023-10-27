import math
import json
import os
import random
from datetime import datetime
from os.path import exists

FILE_PATH = "bank.json"

def get_data():
    if not exists(FILE_PATH):
        return {}
    f = open(FILE_PATH, "r")
    data = f.read()
    return json.loads(data)

def set_data(data):
    f = open(FILE_PATH, "w")
    json_data = json.dumps(data)
    f.write(json_data)

def get_users_as_list():
    result = []
    users = get_data()
    for user_account_number in users:
        user_data = users[user_account_number]
        user_data["account_number"] = user_account_number
        result.append(user_data)
    results_as_ll = list_to_linked_list(result)
    return results_as_ll

class LinkedList:
    def __init__(self, _value, _next):
        self.value = _value
        self.next = _next

    def index(self, index):
        if index == 0:
            return self.value
        else:
            if self.next is None:  # Check if self.next is None
                return None
            else:
                return self.next.index(index - 1)

    def set_index(self, index, value):
        if index == 0:
            self.value = value
        else:
            if self.next is not None:  # Check if self.next is not None
                self.next.set_index(index - 1, value)

    def size(self):
        if self.next is None:
            return 1
        else:
            return 1 + self.next.size()

    def append(self, x):
        if self.next is None:
            self.next = LinkedList(x, None)
        else:
            self.next.append(x)

def list_to_linked_list(arr):
    n = None
    for i in range(len(arr) - 1, -1, -1):
        node = LinkedList(arr[i], n)
        n = node
    return n

def heap_sort(input_list, field):
    range_start = int((input_list.size() - 2) / 2)
    for start in range(range_start, -1, -1):
        sift_down(input_list, field, start, input_list.size() - 1)

    range_start = int(input_list.size() - 1)
    for end_index in range_start, 0, -1:
        swap(input_list, end_index, 0)
        sift_down(input_list, field, 0, end_index - 1)
    return input_list

def swap(input_list, a, b):
    a_value = input_list.index(a)
    if a_value is not None:
        b_value = input_list.index(b)
        if b_value is not None:
            input_list.set_index(a, b_value)
            input_list.set_index(b, a_value)

def sift_down(input_list, field, start_index, end_index):
    """
    The "Sift Down" function of the heap sort algorithm,
    customized to also include object fields.
    """
    root_index = start_index
    while True:
        child = root_index * 2 + 1
        if child > end_index:
            break
        if child + 1 <= end_index and input_list.index(child)[field] < input_list.index(child + 1)[field]:
            child += 1
        if input_list.index(root_index)[field] < input_list.index(child)[field]:
            swap(input_list, child, root_index)
            root_index = child
        else:
            break

# ─── BINARY SEARCH ──────────────────────────────────────────────────────────────

def text_binary_search(input_list, field, query):
    """
    A custom binary search implementation that:
    (1) Assumes the input_list to have elements of type object
        and then sorts by a common key in all those objects name
        "field"
    (2) Make the text lowercase and trims the text in the fields
    so for example "foo bar" can match "FooBar"
    """
    low = 0
    high = input_list.size() - 1
    query = make_text_searchable(query)
    while low <= high:
        mid = math.floor((low + high) / 2)
        if make_text_searchable(input_list.index(mid)[field]) > query:
            high = mid - 1
        elif make_text_searchable(input_list.index(mid)[field]) < query:
            low = mid + 1
        else:
            return mid
    return -1

def make_text_searchable(text):
    """
    Make the text lowercase the text and removes spaces
    """
    return text.lower().replace(" ", "")

# ─── ACCOUNT NUMBER ─────────────────────────────────────────────────────────────

def generate_account_number():
    """
    Generates a new unique account number. The bank
    prefix number is 1717 2424, the 8 other digits are
    then generated randomly
    """
    prefix = "17172424"
    result = ""
    for _ in range(0, 8):
        random_number = random.randint(1, 9)
        result += str(random_number)
    return prefix + result

# ─── TRANSACTION ────────────────────────────────────────────────────────────────

def make_transaction():
    choice = input("Would you like to make a transaction? (Yes or No): ").strip().lower()
    if choice == "no":
        return
    elif choice == "yes":
        account_number = input("Enter your account number: ")
        users = get_data()
        if account_number in users:
            display_account_balance(account_number)
            transaction_type = input("Would you like to make a deposit or withdrawal? (Deposit or Withdraw): ").strip().lower()
            if transaction_type == "deposit":
                amount = float(input("Enter the amount you would like to deposit: "))
                deposit(account_number, amount)
                display_account_balance(account_number)
            elif transaction_type == "withdraw":
                amount = float(input("Enter the amount you would like to withdraw: "))
                withdrawal(account_number, amount)
                display_account_balance(account_number)
            else:
                print("Invalid choice. Please enter 'Deposit' or 'Withdraw'.")
        else:
            print("Account not found.")
            create_account_choice = input("Would you like to create a new account? (Yes or No): ").strip().lower()
            if create_account_choice == "yes":
                create_new_account_option()

def create_new_account_option():
    user_name = input("Full Name: ")
    balance = float(input("Balance: "))
    gender = input("Gender: ")
    city = input("City of Residence: ")
    phone_number = input("Phone Number: ")
    create_new_user(user_name, balance, gender, city, phone_number)

def display_account_balance(account_number):
    """
    Displays the current balance for the given account.
    """
    users = get_data()
    if account_number in users:
        balance = users[account_number]["balance"]
        print("Your current balance is:", balance)
    else:
        print("Account not found.")

def deposit(account_number, amount):
    """
    Deposits the specified amount into the user's account.
    """
    users = get_data()
    if account_number in users:
        users[account_number]["balance"] += amount
        set_data(users)
        print("Deposited R",amount, "into your account.")
    else:
        print("Account not found.")


def withdrawal(account_number, amount):
    """
    Performs a withdrawal from the user's account.
    """
    users = get_data()
    if account_number in users:
        if users[account_number]["balance"] >= amount:
            users[account_number]["balance"] -= amount
            set_data(users)
            print("Withdrawn R", amount, "from your account.")
        else:
            print("Insufficient balance for withdrawal.")
    else:
        print("Account not found.")

# ─── update information ──────────────────────────────────────────────────────────

def update_information(account_number):
    """
    Given an account number, this asks the user what to change and then
    changes the properties of that.
    """
    users = get_data()
    account_number = account_number.strip()  # Remove leading/trailing spaces
    print_horizontal_line()
    print("► 1 ∙ Full Name ")
    print_horizontal_line()
    print("► 2 ∙ Gender ")
    print_horizontal_line()
    print("► 3 ∙ City ")
    print_horizontal_line()
    print("► 4 ∙ Phone Number ")
    print_horizontal_line()
    command = int(input("What to change? "))
    print_horizontal_line()
    if command == 1:
        new_name = input("New Full Name: ")
        users[account_number]["full_name"] = new_name
    if command == 2:
        new_gender = input("New Gender: ")
        users[account_number]["gender"] = new_gender
    if command == 3:
        new_city = input("New City: ")
        users[account_number]["city"] = new_city
    if command == 4:
        new_phone_number = input("New Phone Number: ")
        users[account_number]["phone_number"] = new_phone_number

    set_data(users)
    clean_terminal_screen()
    display_account_information_by_given_account_number(account_number)

# ─── CREATE A NEW USER ──────────────────────────────────────────────────────────

def create_new_user(full_name, balance, gender, city, phone_number):
    """
    Creates a new user with the given information
    """
    users = get_data()
    date = datetime.today().strftime('%Y-%m-%d')
    account_number = generate_account_number()
    users[account_number] = {
        "full_name": full_name,
        "gender": gender,
        "balance": balance,
        "account_creation_date": date,
        "city": city,
        "phone_number": phone_number
    }
    set_data(users)
    display_account_information_by_given_account_number(account_number)

# ─── SEARCH ACCOUNT ─────────────────────────────────────────────────────────────

def search_account(field, query):
    """
    Searches the "query" from the user data in the "field" fields
    """
    users = get_users_as_list()
    users = heap_sort(users, field)
    index = text_binary_search(users, field, query)
    if index == -1:
        print("──── Error ──────────────────────────────────")
        print("Found no one as", query)
    else:
        user = users.index(index)
        display_user_object(user, user["account_number"])

# ─── DELETE AN ACCOUNT ──────────────────────────────────────────────────────────

def delete_account(account_number):
    """
    Deletes an account if exists, otherwise displays an error
    """
    users = get_data()
    if account_number not in users:
        print("Did not find the account with number: " + account_number)
        return
    del users[account_number]
    set_data(users)
    print("Account number", account_number, "removed.")

# ─── INTERFACE TOOLS ────────────────────────────────────────────────────────────

def clean_terminal_screen():
    """
    Cleans the terminal screen by performing a system
    clear command. Cls on windows and Clear on UNIX ones.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def print_horizontal_line():
    """
    A pretty decorative horizontal line.
    """
    print("─────────────────────────────────────────────")

# ─── DISPLAY USER OBJECT ────────────────────────────────────────────────────────

def display_account_information_by_given_account_number(account_number):
    """
    Displays the information about a given account number
    """
    users = get_data()
    user = users[account_number]
    display_user_object(user, account_number)

def display_user_object(user_object, account_number):
    """
    Displays a single user object. The account_number is taken
    separately since there can be either a list input or a dictionary
    input. In a list input the account_number is within the user object
    and in the dictionary form the account_number is the key mapped
    to the dictionary
    """
    print_horizontal_line()
    print("Full name:      ", user_object["full_name"])
    print("Account number: ", account_number)
    print("Created at:     ", user_object["account_creation_date"])
    print("Balance:        ", user_object["balance"])
    print("Gender:         ", user_object["gender"])
    print("City:           ", user_object["city"])
    print("Phone:          ", user_object["phone_number"])

def display_all_accounts_sorted_by(field):
    """
    Displays all the users one after the other, sorted by a given field
    """
    users = get_users_as_list()
    users = heap_sort(users, field)
    clean_terminal_screen()
    for i in range(0, users.size()):
        user = users.index(i)
        display_user_object(user, user["account_number"])

def beatify_field_name(field):
    if field == "full_name":
        return "Full Name"
    if field == "account_creation_date":
        return "Account Creation Data"
    if field == "city":
        return "City"
    if field == "gender":
        return "Gender"
    if field == "phone_number":
        return "Phone Number"
    return "Unknown"

def ask_user_what_field_to_sort_the_display_by():
    """
    Shows a menu so that the user cas pick a field to sort the data by.
    """
    print("Sorting by:")
    print_horizontal_line()
    print("► 1 ∙ Full Name ")
    print_horizontal_line()
    print("► 2 ∙ Gender ")
    print_horizontal_line()
    print("► 3 ∙ City ")
    print_horizontal_line()
    print("► 4 ∙ Phone Number ")
    print_horizontal_line()
    print("► 5 ∙ Account Creating Date ")
    print_horizontal_line()
    print("► 6 ∙ Account Number ")
    print()
    command = input("Your option: ")
    if command == "1":
        return "full_name"
    if command == "2":
        return "gender"
    if command == "3":
        return "city"
    if command == "4":
        return "phone_number"
    if command == "5":
        return "account_creation_date"
    if command == "6":
        return "account_number"
    return "full_name"

# ─── DISPLAY MENU ───────────────────────────────────────────────────────────────

def display_menu():
    """
    Displays the welcome menu and asks the user for a
    command to perform (which then performs).

    This also acts as the UI and receives the information
    regarding of the respective functions.
    """
    clean_terminal_screen()

    print()

    print("  ╭───────────────────────╮           ")
    print("  │ ▶︎ 1 • Create Account  │           ")
    print("  ├───────────────────────┴─────╮     ")
    print("  │ ▶︎ 2 • Perform Transaction   │     ")
    print("  ├────────────────────────────┬╯     ")
    print("  │ ▶︎ 3 • Update Account Info  │      ")
    print("  ├───────────────────────┬────╯      ")
    print("  │ ▶︎ 4 • Delete Account  │           ")
    print("  ├───────────────────────┴────╮      ")
    print("  │ ▶︎ 5 • Search Account Info  │      ")
    print("  ├────────────────────────────┴╮     ")
    print("  │ ▶︎ 6 • View Customer's List  │     ")
    print("  ├────────────────────┬────────╯     ")
    print("  │ ▶︎ 7 • Exit System  │              ")
    print("  ╰────────────────────╯              ")

    user_choice = int(input("\n  ☞ Enter your command: "))

    clean_terminal_screen()

    if user_choice == 1:
        print("── Creating a new user ──────────────────────")
        user_name = input("Full Name: ")
        balance = float(input("Balance: "))
        gender = input("Gender: ")
        city = input("City of Residence: ")
        phone_number = input("Phone Number: ")
        create_new_user(user_name, balance, gender, city, phone_number)

    if user_choice == 2:
        print("── Requesting Transaction ───────────────────")
        make_transaction()

    if user_choice == 3:
        print("── Changing Account Information ─────────────")
        account_number = input("Account Number To Change: ")
        update_information(account_number)

    if user_choice == 4:
        print("── Deleting an Account ──────────────────────")
        account_number = input("Account number to delete: ")
        delete_account(account_number)

    if user_choice == 5:
        print("── Search Account ───────────────────────────")
        query = input("Searching for: ")
        clean_terminal_screen()
        search_account("full_name", query)

    if user_choice == 6:
        print("── Displaying all Accounts ──────────────────")
        field = ask_user_what_field_to_sort_the_display_by()
        display_all_accounts_sorted_by(field)

        print("\n\nSorted by user", beatify_field_name(field))

    if user_choice == 7:
        quit()

    print()
    print_horizontal_line()
    input("PRESS ENTER TO CONTINUE ")
    print()

# ─── MAIN ───────────────────────────────────────────────────────────────────────

while True:
    display_menu()

