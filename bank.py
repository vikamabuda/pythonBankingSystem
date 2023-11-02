import re
import os
import random

USERS_FILE = "users.txt"
TRANSACTIONS_FILE = "transactions.txt"



def save_users(users):
    with open(USERS_FILE, "w") as f:
        for username, user_data in users.items():
            f.write(f"{username}:{user_data['password']}\n")

def load_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) == 2:  # Check if there are 2 values in the line
                    username, password = parts
                    users[username] = {"password": password, "accounts": {}}
                else:
                    print(f"Skipping line: {line} due to incorrect format.")
    return users

def save_transactions(transactions):
    with open(TRANSACTIONS_FILE, "w") as f:
        for username, user_data in transactions.items():
            for account_number, account in user_data["accounts"].items():
                f.write(f"{username}:{account_number}:{account['balance']}:{account['gender']}:{account['city']}:{account['phone_number']}:{account['full_name']}\n")

def load_transactions():
    transactions = {}
    if os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) == 7:  # Check if there are 7 values in the line
                    username, account_number, balance, gender, city, phone_number, full_name = parts
                    if username not in transactions:
                        transactions[username] = {"accounts": {}}
                    transactions[username]["accounts"][account_number] = {
                        "account_number": account_number,
                        "balance": float(balance),
                        "gender": gender,
                        "city": city,
                        "phone_number": phone_number,
                        "full_name": full_name
                    }
                else:
                    print(f"Skipping line: {line} due to incorrect format.")
    return transactions
def get_data():
    users = load_users()
    transactions = load_transactions()
    for username, data in users.items():
        if username in transactions:
            data["accounts"] = transactions[username]["accounts"]
    return users

def set_data(data):
    users = {}
    transactions = {}
    for username, user_data in data.items():
        users[username] = {"password": user_data["password"]}
        transactions[username] = {"accounts": user_data["accounts"]}
    save_users(users)
    save_transactions(transactions)


def register_user():
    users = get_data()

    while True:
        username = input("Enter a username: ")

        if username in users:
            print("Username already exists. Please choose another one.")
        else:
            password = input("Enter a password: ")

            # Password validation using regular expression
            password_pattern = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
            if not re.match(password_pattern, password):
                print("Password must contain at least 1 letter, 1 digit, and be at least 8 characters long.")
                continue

            phone_number = input("Phone Number (10 digits): ")

            # Phone number validation using regular expression
            phone_pattern = r"^\d{10}$"
            if not re.match(phone_pattern, phone_number):
                print("Invalid phone number format. Please use 10 digits without the '+' symbol.")
                continue

            users[username] = {"password": password, "accounts": {}}
            set_data(users)
            print("User registered successfully. \U0001F917")
            break


def login():
    users = get_data()
    while True:
        username = input("Enter your username: ")
        if username in users:
            password = input("Enter your password: ")
            if users[username]["password"] == password:
                print("Login successful!")
                return username
            else:
                print("Incorrect password. Please try again.")
        else:
            print("Username not found. Please register or try again.")


class BankAccount:
    def __init__(self, account_number, full_name, balance, gender, city, phone_number):
        self.account_number = account_number
        self.full_name = full_name
        self.balance = balance
        self.gender = gender
        self.city = city
        self.phone_number = phone_number


def create_new_account_option(username):
    users = get_data()
    user_data = users[username]

    full_name = input("Full Name: ")
    balance = float(input("Balance: "))
    gender = input("Gender: ")
    city = input("City of Residence: ")

    while True:
        phone_number = input("Phone Number (10 digits): ")

        # Phone number validation using regular expression
        phone_pattern = r"^\d{10}$"
        if not re.match(phone_pattern, phone_number):
            print("Invalid phone number format. Please use 10 digits without the '+' symbol.")
            continue
        else:
            break

    account_number = generate_account_number()
    new_account = BankAccount(account_number, full_name, balance, gender, city, phone_number)
    user_data["accounts"][account_number] = vars(new_account)
    set_data(users)
    print("Account created successfully.")
    print("Account Details:")
    display_account_balance(vars(new_account))


def display_account_balance(account):
    print("Account Number:", account["account_number"])
    print("Full Name:", account["full_name"])
    print("Balance:", account["balance"])
    print("Gender:", account["gender"])
    print("City of Residence:", account["city"])
    print("Phone Number:", account["phone_number"])


def make_transaction(username):
    users = get_data()
    user_data = users[username]

    account_number = input("Enter your account number: ")
    if account_number in user_data["accounts"]:
        account = user_data["accounts"][account_number]
        display_account_balance(account)

        transaction_type = input(
            "Would you like to make a deposit or withdrawal? (Deposit or Withdraw): ").strip().lower()
        if transaction_type == "deposit":
            amount = float(input("Enter the amount you would like to deposit: "))
            account["balance"] += amount
            set_data(users)
            print("Deposited R", amount, "into your account.")
        elif transaction_type == "withdraw":
            amount = float(input("Enter the amount you would like to withdraw: "))
            if account["balance"] >= amount:
                account["balance"] -= amount
                set_data(users)
                print("Withdrawn R", amount, "from your account.")
            else:
                print("Insufficient balance for withdrawal.")
        else:
            print("Invalid choice. Please enter 'Deposit' or 'Withdraw'.")
    else:
        print("Account not found.")


def update_information(username):
    users = get_data()
    user_data = users[username]

    account_number = input("Enter the account number to update: ")
    if account_number in user_data["accounts"]:
        account = user_data["accounts"][account_number]
        print("Current Account Information:")
        display_account_balance(account)
        print("Choose the information to update:")
        print("1. Full Name")
        print("2. Gender")
        print("3. City of Residence")
        print("4. Phone Number")
        choice = input("Enter the number of the information to update: ")
        if choice == "1":
            new_name = input("New Full Name: ")
            account["full_name"] = new_name
        elif choice == "2":
            new_gender = input("New Gender: ")
            account["gender"] = new_gender
        elif choice == "3":
            new_city = input("New City of Residence: ")
            account["city"] = new_city
        elif choice == "4":
            new_phone_number = input("New Phone Number: ")
            account["phone_number"] = new_phone_number
        set_data(users)
        print("Account information updated successfully.")
    else:
        print("Account not found.")


def generate_account_number():
    prefix = "17172424"
    result = ""
    for _ in range(0, 8):
        random_number = random.randint(1, 9)
        result += str(random_number)
    return prefix + result


def search_account(username, field, query):
    users = get_data()
    user_data = users[username]
    results = []
    for account_number, account in user_data["accounts"].items():
        if query.lower() in account[field].lower():
            results.append(account)

    if len(results) == 0:
        print("No matching accounts found.")
    else:
        for account in results:
            display_account_balance(account)


def delete_account(username, account_number):
    users = get_data()
    user_data = users[username]
    if account_number in user_data["accounts"]:
        del user_data["accounts"][account_number]
        set_data(users)
        print("Account number", account_number, "removed.")
    else:
        print("Account not found.")


def display_all_accounts_sorted_by(username, field):
    users = get_data()
    user_data = users[username]
    accounts = user_data["accounts"]
    accounts = sorted(accounts.values(), key=lambda x: x[field])

    for account in accounts:
        display_account_balance(account)


def ask_user_what_field_to_sort_the_display_by():
    print("Sort accounts by:")
    print("1. Full Name")
    print("2. Gender")
    print("3. City of Residence")
    print("4. Phone Number")
    choice = input("Enter the number of the field to sort by: ")
    if choice == "1":
        return "full_name"
    elif choice == "2":
        return "gender"
    elif choice == "3":
        return "city"
    elif choice == "4":
        return "phone_number"
    else:
        return "full_name"


def main():
    while True:
        print("Welcome to the Bank System \U0001F917")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            register_user()
        elif choice == "2":
            username = login()
            while True:
                print("\nWelcome, " + username + "!")
                print("1. Create Account")
                print("2. Perform Transaction")
                print("3. Update Account Info")
                print("4. Delete Account")
                print("5. Search Account Info")
                print("6. View Customer's List")
                print("7. Logout")
                option = input("Enter your option: ")
                if option == "1":
                    create_new_account_option(username)
                elif option == "2":
                    make_transaction(username)
                elif option == "3":
                    update_information(username)
                elif option == "4":
                    account_number = input("Enter the account number to delete: ")
                    delete_account(username, account_number)
                elif option == "5":
                    field = input(
                        "Enter the field to search by (Full Name, Gender, City, Phone Number): ").strip().lower()
                    query = input("Enter the search query: ")
                    search_account(username, field, query)
                elif option == "6":
                    field = ask_user_what_field_to_sort_the_display_by()
                    display_all_accounts_sorted_by(username, field)
                elif option == "7":
                    print("Logging out.")
                    break
                else:
                    print("Invalid option. Please try again.")
        elif choice == "3":
            print("Exiting the Bank System.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()


