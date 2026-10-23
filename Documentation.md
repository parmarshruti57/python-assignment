# Riverstone Micro-Banking & Audit Engine

## Project overview

This project implements a command-line transactional banking and audit program in Python 3. It is based on the supplied Software Requirements Specification (SRS), with renamed example data, identifiers, variables, and sample values.

The program is designed as one source file, `main.py`, and uses only the permitted `datetime` module. It does not use third-party packages or a database engine.

## Files created at runtime

| File | Purpose |
|---|---|
| `accounts.db` | Plain-text account records: account ID, account type, balance |
| `ledger.txt` | Timestamped successful actions |
| `errors.log` | Timestamped error and rejected-operation messages |

The program creates a small sample `accounts.db` when the file is missing. Existing database files are not overwritten by that setup function.

## How to run

1. Save `main.py` and `Documentation.md` in the same folder.
2. Open a terminal or command prompt in that folder.
3. Run:

   ```bash
   python main.py
   ```

4. The demonstrations run first. The interactive menu then offers compound interest, penalty calculation, a trajectory-guard demonstration, and exit.

## Main menu

- **1 — Compound interest:** asks for a starting amount, rate, and number of periods. Each period is calculated using a loop.
- **2 — Penalty calculation:** calculates a percentage penalty using arithmetic.
- **3 — Trajectory guard:** applies transaction changes until a stop flag is found or the current balance is below the safety floor.
- **4 — Exit:** ends the interactive loop.

Invalid menu selections and invalid numeric inputs are handled without terminating the program.

## Architecture diagram

```text
                         +----------------------+
                         |       main.py        |
                         +----------+-----------+
                                    |
            +-----------------------+-----------------------+
            |                       |                       |
   +--------v--------+     +--------v--------+     +--------v--------+
   | State / CLI     |     | Parser / Audit  |     | Reverse Index /  |
   | interest, guard |     | parser, closure |     | Queue cleaning  |
   +-----------------+     +-----------------+     +-----------------+
            |                       |                       |
            +-----------------------+-----------------------+
                                    |
                         +----------v-----------+
                         | File / Logging       |
                         | accounts.db, logs    |
                         +----------+-----------+
                                    |
                         +----------v-----------+
                         | Account class         |
                         | Savings / Current /   |
                         | Credit polymorphism  |
                         +-----------------------+
```

## Module guide

### 1. State control and trajectory guards

- `compound_amount(principal, rate_percent, periods)` calculates compound growth through a `while` loop.
- `calculate_penalty(amount, penalty_rate)` returns the percentage penalty.
- `trajectory_guard(transactions, opening_balance, safety_floor)` processes transaction dictionaries and stops early if a stop flag is true or the running balance is below the safety floor.
- `command_loop()` repeatedly displays the menu until the user chooses exit.

### 2. Manual parser and closures

- `parse_raw_log_line(line, delimiter=",", quote_char='"')` scans one character at a time. Delimiters inside quotes remain part of a field, doubled quotes inside quoted text become one quote, and empty/trailing fields are retained.
- `create_audit_filter(threshold)` returns a nested validation function. Its `nonlocal` counter records the number of validation calls for that particular filter.
- `build_position_filters(criteria_count)` creates lambdas with `k=position` so each lambda remembers the correct position rather than the final loop value.

### 3. Reverse index and in-place queue processing

- `build_reverse_index(branch_records)` maps each service tag to a sorted list of unique `(account_id, branch_id)` pairs.
- `clean_transaction_queue(data_list)` modifies the original outer list. Tuples become lists, embedded lists are sorted in descending order, even integer IDs are removed from sets, and repeated primitive values are removed while preserving the first occurrence.
- The queue demonstration compares `id()` before and after cleaning to show that the outer list object is unchanged.

### 4. File operations and exception logging

The custom exception hierarchy is:

```text
BankingError
├── CorruptedRecordError
├── OutOfBoundsError
└── InsufficientBalanceError
```

- `read_account_records()` validates account rows and logs malformed entries rather than stopping at the first bad row.
- `update_account_balance()` opens the file in `r+` mode and updates the selected record. It uses seek/read/write operations to preserve the remaining file content.
- `log_event()` writes a timestamped line to `ledger.txt` or `errors.log`.
- File access uses `with` blocks so files are closed reliably.

Expected record format:

```text
AC710,SAVINGS,6400.00
AC825,CURRENT,1250.00
AC936,CREDIT,9000.00
```

Supported account types are `SAVINGS`, `CURRENT`, and `CREDIT`.

### 5. Object-oriented design and polymorphism

- `Account` is the base class. It has a protected `_account_id`, private `__balance`, and class attribute `total_accounts`.
- Public getters and setters provide controlled access to the account identifier and balance.
- `SavingsAccount` rejects a settlement that would reduce its balance below 1000.
- `CurrentAccount` permits the balance to go negative only within its private overdraft limit.
- `CreditAccount` adds a 2.5% surcharge before checking the configured credit limit.
- `execute_batch_settlement()` handles each account in its own `try-except`, so one rejected transaction does not stop later accounts.

## State and scope tracking table

| Name | Scope / kind | Purpose |
|---|---|---|
| `running_balance` | Local variable | Current balance while checking a transaction sequence |
| `audited_count` | Enclosing-scope variable | Counter shared with the nested audit function |
| `nonlocal audited_count` | Nonlocal access | Updates the closure counter without a global variable |
| `position` | Loop-local variable | Index used while building positional lambdas |
| `k=position` | Lambda default argument | Prevents late-binding of the final loop value |
| `Account.total_accounts` | Class attribute | Counts constructed account objects |
| `self._account_id` | Protected-style instance attribute | Stores the account identifier |
| `self.__balance` | Private instance attribute | Stores the account balance; Python name-mangles it |
| `self.__overdraft_limit` | Private subclass attribute | Stores the current account overdraft limit |
| `self.__credit_limit` | Private subclass attribute | Stores the credit account limit |

Python name-mangling demonstration: the balance is stored internally as `_Account__balance`. Code should normally use `get_balance()` and `set_balance()` instead of accessing the mangled name directly.

## Example values

The original example identifiers and values have been replaced with these sample values:

| Account ID | Type | Starting balance |
|---|---|---:|
| `AC710` | SAVINGS | 6400.00 |
| `AC825` | CURRENT | 1250.00 |
| `AC936` | CREDIT | 9000.00 |
| `AC104` | SAVINGS | 3200.00 |

These are fictional demonstration records, not real customer information.

## Syllabus compliance checklist

- [x] **Unit 1:** variables, input/output, conditions, nested loops, arithmetic, Boolean short-circuiting in the trajectory guard.
- [x] **Unit 2:** functions, arguments, return values, manual character-by-character parsing, slicing/index tracking, closures, `nonlocal`, lambdas and late-binding prevention.
- [x] **Unit 3:** lists, tuples, sets, dictionaries, comprehensions, sorting, in-place mutation and duplicate removal.
- [x] **Unit 4:** text-file input/output, `with`, `r+`, `seek()`, `read()`, `write()`, `truncate()`, custom exceptions and error logging.
- [x] **Unit 5:** classes, inheritance, `super()`, encapsulation, getters/setters, overriding and polymorphic batch processing.
- [x] **Import policy:** only `datetime` is imported; no third-party packages are required.

## Important implementation notes

1. The SRS requires a hand-written parser, so `parse_raw_log_line()` does not use `split()` or `replace()`.
2. The code does not use `math`, `json`, `csv`, `os`, `sys`, or external packages.
3. `clean_transaction_queue()` preserves the identity of the outer list. Elements inside it may be converted or modified as required.
4. `update_account_balance()` is included as the `r+` update routine. Test it on a copy of `accounts.db` before using it with any important data.
5. The project is an educational demonstration, not a production banking system. It has no authentication, encryption, multi-user concurrency, or real-money processing.

## Quick manual test ideas

1. In the menu, enter `1`, principal `1000`, rate `5`, periods `2`. Expected final amount: `1102.5`.
2. Enter an invalid menu option such as `9`. The program should display an error and return to the menu.
3. Check the parser demonstration: commas inside quoted fields should remain within a single parsed field.
4. Check the queue demonstration: it should print `Same list object: True`.
5. In the batch settlement demonstration, one rejected savings transaction should not prevent the remaining accounts from being processed.
