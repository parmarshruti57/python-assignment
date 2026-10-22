class BankAccount:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance = self.balance + amount
            print("Deposit successful.")
        else:
            print("Enter a positive amount.")

    def display(self):
        print("Account holder:", self.name)
        print("Balance:", self.balance)

account = BankAccount("Neha", 1000)
account.deposit(500)
account.display()
