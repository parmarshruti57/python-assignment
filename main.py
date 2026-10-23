"""
PTMAE - Pure Python Transactional Micro-Banking & Audit Engine
Student implementation for Python Units 1-5.
Only the permitted datetime module is imported.
"""

from datetime import datetime


# --------------------------- Module 1: State engine ---------------------------

def compound_amount(principal, rate_percent, periods):
    """Calculate compound amount using arithmetic operators and loops."""
    amount = principal
    step = 0
    while step < periods:
        amount = amount + amount * rate_percent / 100
        step += 1
    return amount


def calculate_penalty(amount, penalty_rate):
    """Calculate a simple penalty without importing math."""
    return amount * penalty_rate / 100


def trajectory_guard(transactions, opening_balance, safety_floor=250):
    """Stop at the first termination flag or balance below the safety floor."""
    running_balance = opening_balance
    processed = []
    for entry in transactions:
        stop_flag = entry.get("stop", False)
        change = entry.get("amount", 0)
        if stop_flag or running_balance < safety_floor:
            break
        running_balance += change
        processed.append((entry.get("label", "unnamed"), running_balance))
    return running_balance, processed


def command_loop():
    """Interactive menu; invalid commands return to the menu."""
    while True:
        print("\n=== Riverstone Micro-Banking ===")
        print("1. Compound interest")
        print("2. Calculate penalty")
        print("3. Show trajectory guard demo")
        print("4. Exit")
        choice = input("Choose 1-4: ").strip()
        if choice == "1":
            try:
                principal = float(input("Opening amount: "))
                rate = float(input("Annual rate (%): "))
                years = int(input("Number of periods: "))
                if principal < 0 or rate < 0 or years < 0:
                    print("Values must be non-negative.")
                    continue
                print("Final amount:", round(compound_amount(principal, rate, years), 2))
            except ValueError:
                print("Please enter valid numeric values.")
        elif choice == "2":
            try:
                amount = float(input("Transaction amount: "))
                rate = float(input("Penalty rate (%): "))
                if amount < 0 or rate < 0:
                    print("Values must be non-negative.")
                    continue
                print("Penalty:", round(calculate_penalty(amount, rate), 2))
            except ValueError:
                print("Please enter valid numeric values.")
        elif choice == "3":
            sample = [
                {"label": "cash-in", "amount": 500},
                {"label": "service-fee", "amount": -180},
                {"label": "large-payment", "amount": -700},
                {"label": "not-reached", "amount": 100}
            ]
            balance, history = trajectory_guard(sample, 800, 250)
            print("Processed:", history)
            print("Ending balance:", balance)
        elif choice == "4":
            print("Session closed.")
            break
        else:
            print("Unknown command. Choose a number from 1 to 4.")


# ------------------------ Module 2: parser and closures ----------------------

def parse_raw_log_line(line, delimiter=",", quote_char='"'):
    """Parse a delimited line manually; quoted delimiters remain field data."""
    fields = []
    current = ""
    inside_quotes = False
    position = 0
    while position < len(line):
        char = line[position]
        if char == quote_char:
            if inside_quotes and position + 1 < len(line) and line[position + 1] == quote_char:
                current += quote_char
                position += 2
                continue
            inside_quotes = not inside_quotes
        elif char == delimiter and not inside_quotes:
            fields.append(current)
            current = ""
        else:
            current += char
        position += 1
    fields.append(current)
    return fields


def create_audit_filter(threshold):
    """Return a validator with a private call counter captured by closure."""
    audited_count = 0

    def validate(record):
        nonlocal audited_count
        audited_count += 1
        try:
            value = float(record.get("amount", 0))
        except (ValueError, TypeError):
            return False
        return value >= threshold

    def count():
        return audited_count

    validate.audit_count = count
    return validate


def build_position_filters(criteria_count):
    """Create positional filters without late-binding errors."""
    filters = []
    for position in range(criteria_count):
        filters.append(lambda row, k=position: len(row) > k and bool(row[k]))
    return filters


# ---------------------- Module 3: inversion and queues -----------------------

def build_reverse_index(branch_records):
    """Map each service to sorted, unique (account, branch) pairs."""
    return {
        service: sorted({
            (account_id, branch_id)
            for branch_id, records in branch_records.items()
            for account_id, services in records
            if service in services
        })
        for service in {
            service
            for records in branch_records.values()
            for account_id, services in records
            for service in services
        }
    }


def clean_transaction_queue(data_list):
    """Clean the same top-level list object in place."""
    for index in range(len(data_list)):
        item = data_list[index]
        if isinstance(item, tuple):
            data_list[index] = list(item)
            item = data_list[index]
        if isinstance(item, set):
            even_ids = set()
            for transaction_id in item:
                if isinstance(transaction_id, int) and transaction_id % 2 == 0:
                    even_ids.add(transaction_id)
            data_list[index] = item - even_ids
        elif isinstance(item, list):
            item.sort(reverse=True)
        elif isinstance(item, int):
            pass

    # Remove duplicate primitive values by scanning and deleting in place.
    first = 0
    while first < len(data_list):
        value = data_list[first]
        if isinstance(value, (str, int, float, bool)):
            later = first + 1
            while later < len(data_list):
                if type(data_list[later]) is type(value) and data_list[later] == value:
                    del data_list[later]
                else:
                    later += 1
        first += 1
    return data_list


# ------------------------ Module 4: file and logging -------------------------

class BankingError(Exception):
    """Base class for banking-engine errors."""


class CorruptedRecordError(BankingError):
    """Raised when a database row does not follow the required format."""


class OutOfBoundsError(BankingError):
    """Raised when a requested value exceeds a permitted limit."""


class InsufficientBalanceError(BankingError):
    """Raised when an account cannot cover a settlement."""


def log_event(message, error=False):
    """Append a timestamped message to the appropriate text log."""
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    destination = "errors.log" if error else "ledger.txt"
    with open(destination, "a", encoding="utf-8") as log_file:
        log_file.write(stamp + " | " + message + "\n")


def read_account_records(path="accounts.db"):
    """Read and validate database rows. Invalid rows are logged and skipped."""
    records = []
    try:
        with open(path, "r", encoding="utf-8") as db_file:
            line_number = 0
            for raw_line in db_file:
                line_number += 1
                line = raw_line.rstrip("\n")
                if not line:
                    continue
                parts = parse_raw_log_line(line)
                if len(parts) != 3:
                    log_event("Line " + str(line_number) + ": wrong field count", True)
                    continue
                account_id = parts[0].strip()
                account_type = parts[1].strip().upper()
                try:
                    balance = float(parts[2].strip())
                except ValueError:
                    log_event("Line " + str(line_number) + ": non-numeric balance", True)
                    continue
                if account_type not in ("SAVINGS", "CURRENT", "CREDIT"):
                    log_event("Line " + str(line_number) + ": unknown account type", True)
                    continue
                records.append([account_id, account_type, balance])
    except FileNotFoundError:
        log_event("Database not found; a new file will be created.", True)
    return records


def update_account_balance(path, target_id, new_balance):
    """Update one record using r+ and shift the tail in chunks if its length changes."""
    try:
        with open(path, "r+", encoding="utf-8") as db_file:
            original_lines = []
            for line in db_file:
                original_lines.append(line)
            start = 0
            found = False
            old_line = ""
            for line in original_lines:
                parsed = parse_raw_log_line(line.rstrip("\n"))
                if len(parsed) == 3 and parsed[0].strip() == target_id:
                    old_line = line
                    found = True
                    break
                start += len(line)
            if not found:
                raise OutOfBoundsError("Account ID was not found: " + target_id)

            parsed = parse_raw_log_line(old_line.rstrip("\n"))
            replacement = parsed[0].strip() + "," + parsed[1].strip() + "," + format(new_balance, ".2f") + "\n"
            old_length = len(old_line)
            new_length = len(replacement)
            db_file.seek(start)
            if new_length <= old_length:
                db_file.write(replacement)
                db_file.write(" " * (old_length - new_length))
                db_file.seek(start + old_length)
                # Preserve the existing tail; padding is not a valid record, so compact it.
                tail = db_file.read()
                db_file.seek(start + new_length)
                db_file.write(tail)
                db_file.truncate()
            else:
                # Extend by shifting the tail backwards in bounded chunks.
                db_file.seek(start + old_length)
                tail_chunks = []
                while True:
                    chunk = db_file.read(4096)
                    if not chunk:
                        break
                    tail_chunks.append(chunk)
                tail_text = "".join(tail_chunks)
                db_file.seek(start + new_length)
                db_file.write(tail_text)
                db_file.seek(start)
                db_file.write(replacement)
                db_file.truncate()
        log_event("Updated " + target_id + " to " + format(new_balance, ".2f"))
        return True
    except (OSError, BankingError) as error:
        log_event(str(error), True)
        raise


def create_demo_database(path="accounts.db"):
    """Create sample records only when the database does not exist."""
    try:
        with open(path, "r", encoding="utf-8"):
            return
    except FileNotFoundError:
        with open(path, "w", encoding="utf-8") as db_file:
            db_file.write("AC710,SAVINGS,6400.00\n")
            db_file.write("AC825,CURRENT,1250.00\n")
            db_file.write("AC936,CREDIT,9000.00\n")
            db_file.write("AC104,SAVINGS,3200.00\n")


# ------------------------ Module 5: OOP and settlement -----------------------

class Account:
    total_accounts = 0

    def __init__(self, account_id, balance):
        self._account_id = account_id
        self.__balance = 0.0
        self.set_balance(balance)
        Account.total_accounts += 1

    def get_account_id(self):
        return self._account_id

    def get_balance(self):
        return self.__balance

    def set_balance(self, amount):
        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            raise TypeError("Balance must be numeric.")
        if amount < 0:
            raise OutOfBoundsError("Balance cannot be negative.")
        self.__balance = float(amount)

    def process_settlement(self, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise OutOfBoundsError("Transaction amount must be positive.")
        if self.get_balance() < amount:
            raise InsufficientBalanceError("Insufficient balance.")
        self.set_balance(self.get_balance() - amount)
        return self.get_balance()


class SavingsAccount(Account):
    def process_settlement(self, amount):
        if self.get_balance() - amount < 1000:
            raise InsufficientBalanceError("Savings account must retain at least 1000.")
        return super().process_settlement(amount)


class CurrentAccount(Account):
    def __init__(self, account_id, balance, overdraft_limit=1500):
        super().__init__(account_id, balance)
        self.__overdraft_limit = overdraft_limit

    def process_settlement(self, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise OutOfBoundsError("Transaction amount must be positive.")
        if self.get_balance() + self.__overdraft_limit < amount:
            raise InsufficientBalanceError("Overdraft limit exceeded.")
        self.set_balance(self.get_balance() - amount)
        return self.get_balance()


class CreditAccount(Account):
    def __init__(self, account_id, balance, credit_limit=12000):
        super().__init__(account_id, balance)
        self.__credit_limit = credit_limit

    def process_settlement(self, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise OutOfBoundsError("Transaction amount must be positive.")
        total_due = amount + amount * 2.5 / 100
        if total_due > self.__credit_limit:
            raise OutOfBoundsError("Credit limit exceeded.")
        self.set_balance(self.get_balance() - total_due)
        return self.get_balance()


def execute_batch_settlement(account_list, transaction_amount):
    """Settle each account independently so one failure does not stop the batch."""
    successes = 0
    failures = 0
    for account in account_list:
        try:
            result = account.process_settlement(transaction_amount)
            print(account.get_account_id(), "settled; remaining balance:", round(result, 2))
            log_event(account.get_account_id() + " settlement succeeded")
            successes += 1
        except (BankingError, TypeError, ValueError) as error:
            print(account.get_account_id(), "settlement failed:", str(error))
            log_event(account.get_account_id() + " settlement failed: " + str(error), True)
            failures += 1
    print("Batch complete. Successes:", successes, "| Failures:", failures)
    return successes, failures


# ------------------------------- Demonstrations ------------------------------

def run_demonstrations():
    print("\n--- Parser demonstration ---")
    sample_line = 'AC710,"monthly, deposit","customer ""A""",250'
    print("Input:", sample_line)
    print("Parsed:", parse_raw_log_line(sample_line))

    print("\n--- Closure demonstration ---")
    audit_check = create_audit_filter(100)
    print("Amount 150 accepted:", audit_check({"amount": 150}))
    print("Amount 40 accepted:", audit_check({"amount": 40}))
    print("Audit calls:", audit_check.audit_count())

    print("\n--- Reverse index demonstration ---")
    branch_data = {
        "BRANCH_11": [("AC710", {"SAVINGS", "UPI"}), ("AC825", {"LOAN", "UPI"})],
        "BRANCH_22": [("AC710", {"CARD", "DEPOSIT"}), ("AC936", {"UPI", "DEPOSIT"})]
    }
    print(build_reverse_index(branch_data))

    print("\n--- In-place queue demonstration ---")
    transaction_queue = [(9, 3), [2, 8, 5], {2, 3, 4, 7}, 12, 12, "audit", "audit"]
    before_id = id(transaction_queue)
    print("Before:", transaction_queue)
    clean_transaction_queue(transaction_queue)
    print("After:", transaction_queue)
    print("Same list object:", before_id == id(transaction_queue))

    print("\n--- OOP settlement demonstration ---")
    account_group = [
        SavingsAccount("AC710", 6400),
        CurrentAccount("AC825", 1250, 1500),
        CreditAccount("AC936", 9000, 12000),
        SavingsAccount("AC104", 1200)
    ]
    execute_batch_settlement(account_group, 500)

    print("\n--- File database demonstration ---")
    create_demo_database()
    print("Valid account records:", read_account_records())


if __name__ == "__main__":
    run_demonstrations()
    command_loop()
