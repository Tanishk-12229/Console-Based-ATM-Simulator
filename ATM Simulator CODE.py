import random
import datetime

class User:
    def __init__(self, user_id, pin, balance=0):
        self.user_id = user_id
        self.pin = pin
        self.balance = balance
        self.transaction_history = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited ${amount:.2f} on {self.get_current_datetime()}")

    def withdraw(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew ${amount:.2f} on {self.get_current_datetime()}")

    def transfer(self, recipient, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            recipient.balance += amount
            self.transaction_history.append(f"Transferred ${amount:.2f} to {recipient.user_id} on {self.get_current_datetime()}")
            recipient.transaction_history.append(f"Received ${amount:.2f} from {self.user_id} on {self.get_current_datetime()}")

    def get_transaction_history(self):
        return self.transaction_history

    def get_balance(self):
        return self.balance

    @staticmethod
    def get_current_datetime():
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class ATM:
    def __init__(self):
        self.users = {}
        self.current_user = None

    def add_user(self, user):
        self.users[user.user_id] = user

    def authenticate_user(self, user_id, pin):
        if user_id in self.users and self.users[user_id].pin == pin:
            self.current_user = self.users[user_id]
            return True
        else:
            return False

    def generate_user_id(self):
        while True:
            user_id = str(random.randint(1000, 9999))
            if user_id not in self.users:
                return user_id

    def create_user(self):
        user_id = self.generate_user_id()
        pin = input("Create a 4-digit PIN: ")
        new_user = User(user_id, pin)
        self.add_user(new_user)
        print(f"User ID: {user_id} created successfully. Please remember your user ID and PIN.")

    def main_menu(self):
        while True:
            if not self.current_user:
                print("Welcome to the ATM!")
                user_id = input("Enter your user ID or 'C' to create a new user: ")

                if user_id.lower() == 'c':
                    self.create_user()
                else:
                    pin = input("Enter your PIN: ")
                    if self.authenticate_user(user_id, pin):
                        print(f"Welcome, {self.current_user.user_id}!")

            if self.current_user:
                print("\nATM Menu:")
                print("1. Transaction History")
                print("2. Withdraw")
                print("3. Deposit")
                print("4. Transfer")
                print("5. Check Balance")
                print("6. Change PIN")
                print("7. Logout")

                choice = input("Enter your choice: ")

                if choice == "1":
                    self.show_transaction_history()
                elif choice == "2":
                    self.withdraw()
                elif choice == "3":
                    self.deposit()
                elif choice == "4":
                    self.transfer()
                elif choice == "5":
                    self.check_balance()
                elif choice == "6":
                    self.change_pin()
                elif choice == "7":
                    print("Thank you for using the ATM. Goodbye!")
                    self.current_user = None
                else:
                    print("Invalid choice. Please try again.")

    def show_transaction_history(self):
        transactions = self.current_user.get_transaction_history()
        if transactions:
            print("\nTransaction History:")
            for transaction in transactions:
                print(transaction)
        else:
            print("No transactions found.")

    def withdraw(self):
        amount = float(input("Enter the amount to withdraw: $"))
        if amount > 0:
            self.current_user.withdraw(amount)
            print(f"Withdrew ${amount:.2f} successfully.")
        else:
            print("Invalid amount. Please try again.")

    def deposit(self):
        amount = float(input("Enter the amount to deposit: $"))
        if amount > 0:
            self.current_user.deposit(amount)
            print(f"Deposited ${amount:.2f} successfully.")
        else:
            print("Invalid amount. Please try again.")

    def transfer(self):
        recipient_id = input("Enter the recipient's user ID: ")
        recipient = self.users.get(recipient_id)
        if recipient:
            amount = float(input("Enter the amount to transfer: $"))
            if amount > 0:
                self.current_user.transfer(recipient, amount)
                print(f"Transferred ${amount:.2f} to {recipient.user_id} successfully.")
            else:
                print("Invalid amount. Please try again.")
        else:
            print("Recipient not found.")

    def check_balance(self):
        balance = self.current_user.get_balance()
        print(f"Current Balance: ${balance:.2f}")

    def change_pin(self):
        new_pin = input("Enter a new 4-digit PIN: ")
        if len(new_pin) == 4 and new_pin.isdigit():
            self.current_user.pin = new_pin
            print("PIN changed successfully.")
        else:
            print("Invalid PIN. Please enter a 4-digit numeric PIN.")


def main():
    atm = ATM()
    user1 = User("1234", "1234", 1000.0)
    user2 = User("5678", "5678", 2000.0)
    atm.add_user(user1)
    atm.add_user(user2)
    atm.main_menu()


if __name__ == "__main__":
    main()


