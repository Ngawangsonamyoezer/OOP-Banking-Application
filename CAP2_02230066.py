###########################
# Ngawang Sonam Yoezer
# 1 Electrical
# 02230066
###########################
# REFERENCE
# https://www.youtube.com/watch?v=BRssQPHZMrc&t=6s
# https://www.freecodecamp.org/news/how-to-build-an-online-banking-system-python-oop-tutorial/


import random #This imports the random module, which allows generating random numbers. It's likely used for generating account numbers or passwords.
import string #This imports the string module, which provides a collection of string constants. It's commonly used for generating random strings.

# Abstract Base Class for Accounts
class Account: #This line defines the Account class, which serves as an abstract base class for different types of accounts.
    def __init__(self, account_number, password, account_type, balance): #This is the constructor method (__init__) for the Account class. It initializes the attributes of an account object when it's created.
        self.account_number = account_number # stores the account number, which is a unique identifier for each account.
        self.password = password #stores the password associated with the account, ensuring security.
        self.account_type = account_type # specifies the type of account, such as savings or checking.
        self.balance = balance # stores the balance of the account, representing the amount of money available.

    def deposit(self, amount): # allows depositing a certain amount of money into the account.
        self.balance += amount # Increases the account balance by the deposited amount.

    def withdraw(self, amount): #allows withdrawing a certain amount of money from the account, given that the balance is sufficient.
        if self.balance >= amount: # Checks if the account balance is greater than or equal to the withdrawal amount.
            self.balance -= amount #reduces the account balance by the withdrawn amount
            return True #indicates a successful withdrawal
        else:
            return False #indicates that the withdrawal cannot be completed due to insufficient funds

    def send_money(self, recipient, amount): #This method allows transferring a certain amount of money from the account to another account (recipient's account), given that the balance is sufficient
        if self.balance >= amount: #Checks if the account balance is greater than or equal to the amount to be transferred
            self.balance -= amount # reduces the account balance by the transferred amount
            recipient.balance += amount #increases the balance of the recipient's account by the transferred amount
            return True #ndicates a successful transaction
        else:
            return False #indicates that the transaction cannot be completed due to insufficient funds

    
    def generate_account_number(): #This function generates a random account number 
        return ''.join(random.choices(string.digits, k=5)) #randomly choose digits  and concatenate them together to form a 5-digit account number.

    
    def generate_default_password(): #This function generates a random default password consisting of 4 characters, which can include both letters (upper and lower case) and digits.
        return ''.join(random.choices(string.ascii_letters + string.digits, k=4)) #randomly select characters and concatenate them together to form a 4-character password

# Business Account Class
class BusinessAccount(Account): 
    def __init__(self, account_number, password, balance):
        super().__init__(account_number, password, 'Business', balance) # initializes the account number, password, account type (set as 'Business'), and balance using the superclass's constructor (super().__init__()).


# Personal Account Class
class PersonalAccount(Account):
    def __init__(self, account_number, password, balance):
        super().__init__(account_number, password, 'Personal', balance) #initializes the account number, password, account type (set as 'Personal'), and balance using the superclass's constructor.


# Account Manager for handling account operations and data persistence
class AccountManager:
    
    def open_account(account_type, initial_balance):
        # generate a random account number and password for the new accoun
        account_number = Account.generate_account_number() 
        password = Account.generate_default_password() 

        #checks if the account_type provided is 'business' or 'personal' (case-insensitive). Based on the type, it creates either a BusinessAccount or a PersonalAccount instance using the generated account number, password, and initial balance.

        if account_type.lower() == 'business':
            account = BusinessAccount(account_number, password, initial_balance)
        else:
            account = PersonalAccount(account_number, password, initial_balance)
        
        AccountManager.save_account_info(account) # save the newly created account's information to a file.
        return account #This line returns the newly created account object

    #The function save_account_info writes account information to a file named "accounts.txt". 
    #It takes an account object and a mode parameter (defaults to 'a' for append).
    # The account details, including account number, password, account type, and balance, are written to the file in a comma-separated format, with each account on a new line.
    def save_account_info(account, mode='a'):
        with open('accounts.txt', mode) as file:
            file.write(f"{account.account_number},{account.password},{account.account_type},{account.balance}\n")

#The read_account_info function reads account information from a file named "accounts.txt" and returns a dictionary containing account objects. 
#It opens the file in read mode ('r') and iterates over each line. Each line is split into values using a comma as the delimiter. 
#If a line does not contain exactly four values, it prints a warning and continues to the next line. It converts the balance to a float and creates an account object based on the account type.
# If the file is not found, it prints an error message. Finally, it returns the dictionary of account objects.
    
    def read_account_info():
        accounts = {}
        try:
            with open('accounts.txt', 'r') as file:
                for line in file:
                    values = line.strip().split(',')
                    if len(values) != 4:
                        print(f"Warning: Skipping invalid line in 'accounts.txt': {line.strip()}")
                        continue
                    account_number, password, account_type, balance = values
                    try:
                        balance = float(balance)
                    except ValueError:
                        print(f"Warning: Invalid balance for account {account_number}. Skipping this account.")
                        continue

                    if account_type == 'Business':
                        accounts[account_number] = BusinessAccount(account_number, password, balance)
                    else:
                        accounts[account_number] = PersonalAccount(account_number, password, balance)
        except FileNotFoundError:
            print("Error: The 'accounts.txt' file was not found. Please ensure that the file exists and is in the correct location.")
        return accounts

    #takes a dictionary of accounts and saves them all to the "accounts.txt" file.
    # It iterates through the dictionary values (which are account objects) and uses the save_account_info function from the AccountManager class to save each account
    def save_all_accounts(accounts): 
        with open('accounts.txt', 'w') as file:
            for account in accounts.values():
                AccountManager.save_account_info(account, mode='a')

    #checks if a given account number and password match any account in the accounts stored in "accounts.txt".
    # It does this by calling the read_account_info function from the AccountManager class to retrieve the accounts, then checks if the account number exists in the accounts and if the password matches. 
    #If both conditions are met, it returns the corresponding account object; otherwise, it returns None.
    def login(account_number, password):
        accounts = AccountManager.read_account_info()
        if account_number in accounts and accounts[account_number].password == password:
            return accounts[account_number]
        else:
            return None

    #deletes an account with the given account number from the accounts stored in "accounts.txt". It first retrieves the accounts using the read_account_info function, then checks if the account number exists. 
    #If it does, it deletes the account from the dictionary, saves the updated accounts using save_all_accounts function, and returns True. If the account number does not exist, it returns False.
    def delete_account(account_number):
        accounts = AccountManager.read_account_info()
        if account_number in accounts:
            del accounts[account_number]
            AccountManager.save_all_accounts(accounts)
            return True
        else:
            return False

#If the user chooses to open a new account, they are prompted for the account type (Personal/Business) and initial balance. After creating the account, its details are displayed.
#If the user chooses to login, they are asked for their account number and password. If the login is successful, they are presented with a menu to perform various account operations like checking balance, depositing, withdrawing, sending money, or deleting the account.
#f the user chooses to exit, the program terminates with a farewell message.
def main():
    print("Welcome to the Bank Account System")
    while True:
        print("\nMenu:")
        print("1. Open a new account")
        print("2. Login to existing account")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            account_type = input("Enter the bank type (Personal/Business): ")
            initial_balance = float(input("Enter the initial balance amount: "))
            account = AccountManager.open_account(account_type, initial_balance)
            
            print("Account successfully created!")
            print(f"Account Number: {account.account_number}")
            print(f"Default Password: {account.password}")
            print(f"Bank Type: {account.account_type}")
            print(f"Initial Balance: {account.balance}")
        
        elif choice == '2':
            account_number = input("Enter your account number: ")
            password = input("Enter your password: ")
            
            account = AccountManager.login(account_number, password)
            
            if account:
                print("Login successful!")
                while True:
                    print("\nAccount Menu:")
                    print("1. Check Balance")
                    print("2. Deposit")
                    print("3. Withdraw")
                    print("4. Send Money")
                    print("5. Delete Account")
                    print("6. Logout")
                    acc_choice = input("Enter your choice: ")
                    
                    if acc_choice == '1':
                        print(f"Current Balance: {account.balance}")
                    elif acc_choice == '2':
                        amount = float(input("Enter the amount to deposit: "))
                        account.deposit(amount)
                        AccountManager.save_all_accounts(AccountManager.read_account_info())
                        print(f"Deposited {amount}. New Balance: {account.balance}")
                    elif acc_choice == '3':
                        amount = float(input("Enter the amount to withdraw: "))
                        if account.withdraw(amount):
                            AccountManager.save_all_accounts(AccountManager.read_account_info())
                            print(f"Withdrew {amount}. New Balance: {account.balance}")
                        else:
                            print("Insufficient balance.")
                    elif acc_choice == '4':
                        recipient_account_number = input("Enter the recipient's account number: ")
                        amount = float(input("Enter the amount to send: "))
                        accounts = AccountManager.read_account_info()
                        if recipient_account_number in accounts:
                            recipient_account = accounts[recipient_account_number]
                            if account.send_money(recipient_account, amount):
                                AccountManager.save_all_accounts(accounts)
                                print(f"Sent {amount} to account {recipient_account_number}. New Balance: {account.balance}")
                            else:
                                print("Insufficient balance.")
                        else:
                            print("Recipient account does not exist.")
                    elif acc_choice == '5':
                        confirm = input("Are you sure you want to delete your account? (yes/no): ")
                        if confirm.lower() == 'yes':
                            if AccountManager.delete_account(account.account_number):
                                print("Account deleted successfully.")
                                break
                            else:
                                print("Failed to delete account.")
                    elif acc_choice == '6':
                        print("Logged out successfully.")
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Invalid account number or password.")
        
        elif choice == '3':
            print("Thank you for using the Bank Account System. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

main()
