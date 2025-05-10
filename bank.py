from datetime import datetime

 # setting admin login information
admin_username = "admin"        
admin_password = "admin123"

# file names that are used to store customer, user, transaction informations
customers_file = "customer.txt"
users_file = "user.txt"
transactions_file = "transaction.txt"

# dictionary that holds customer information
customers_dict = {}     

# creating the customers file if it doesnt exist
def create_customers_file():
    try:
        with open(customers_file, 'r') as file: # this reads the file to know if that file already exists
            pass
    except FileNotFoundError:
        with open(customers_file, 'w') as file: # this creates that file 
            pass

# creatning the users file if it doesnt exist
def create_users_file():
    try:
        with open(users_file, 'r') as file:
            pass
    except FileNotFoundError:
        with open(users_file, 'w') as file:
            pass

# creating the transactions file if it doesnt exist
def create_transactions_file():
    try:
        with open(transactions_file, 'r') as file:
            pass
    except FileNotFoundError:
        with open(transactions_file, 'w') as file:
            pass

#loading all customers into dictionary 
def load_customers():           # when the program starts this will load customers into the dictionary
    global customers_dict
    try:
        with open(customers_file, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) != 4:
                    continue
                acc_num, name, address, balance = parts
                customers_dict[acc_num] = {
                    'name': name,
                    'address': address,
                    'balance': float(balance)
                }

    except FileNotFoundError:
        print(f"{customers_file} not found. Creating it")
        create_customers_file()


# saving customrs info from disctionary to file
def save_customers():
    try:
        with open(customers_file, 'w') as file:
            for acc_num, info in customers_dict.items():
                file.write(f"{acc_num},{info['name']},{info['address']},{info['balance']}\n")

    except:
        print(f"Error occured")

# creating a new unique customer id aka account number
def get_customers_id():
    with open(customers_file,'r') as file:
        lines = file.readlines()

        if lines:
            last_line = lines[-1]
            last_id = last_line.split(',')[0]
            last_id_num = last_id[1:]
            next_id_num = int(last_id_num) + 1
            next_id = "C" + f"{next_id_num:03d}"
            return next_id
        
        else:
            return "C001"  # this line makes the count start from C001 if it doesnt already exist

# printing admin menu options
def admin_menu():
    print("\nAdmin Menu:")
    print("1. Create Customer 👨‍💼")
    print("2. Deposit Money 💰")
    print("3. Withdraw Money 💳")
    print("4. Check Balance 💵")
    print("5. Transaction History 📒")
    print("6. Transfer Money 💸")
    print("7. Update Customer 📝")
    print("8. Delete Customer 🗑️")
    print("9. View All Accounts 📑")
    print("10. Exit 🚪")

# printing customer menu options
def customer_menu():
    print("\nCustomer Menu")
    print("1. Deposit Money 💰")
    print("2. Withdraw Money 💳")
    print("3. Check Balance 💵")
    print("4. Transaction History 📒")
    print("5. Transfer Money 💸")
    print("6. Exit 🚪")

# login function for both admin and customers
def login():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

# checking admin login
    if username == admin_username and password == admin_password:
        return "admin", None

#checking customer login from file
    try:
        with open(users_file, 'r') as file:
            lines = file.readlines()
            for things in lines:
                parts = things.strip().split(',')
                if len(parts) != 3:
                    continue
                cus_username = parts[1].strip()
                cus_password = parts[2].strip()

                if password == cus_password and username == cus_username:
                    return "customer", parts[0]

            print(" ❌ Invalid Credentials!")
            return None, None
        
    except FileNotFoundError:
        print(f"{users_file} not found")
        return None, None


# creating a new custtomer 
def create_customer():
    print("Create New Customer")
    name = input("Enter customer name: ")
    username = input("Enter Customer Username: ")

    with open(users_file, 'r') as file:     # this will check if the username already exists
        lines = file.readlines()
        for line in lines:
            if line.strip().split(',')[1] == username:
                print("Username Already Exists")
                return

    password = input("Enter Customer Password: ")
    address = input("Enter Customer Address: ")
    initial_balance = (input("Enter Initial Balance: "))

    try:
        initial_balance = float(initial_balance)
        if initial_balance < 0:
            print("❌ Invalid Balance")
            return
    except ValueError:
        print("❌ Invalid Balance")
        return

    
    initial_balance = float(initial_balance)
    account_number = get_customers_id()

# adding customer to dictionary
    customers_dict[account_number] = {
        'name': name,
        'address': address,
        'balance': initial_balance
    }
    save_customers()

    record_transaction(account_number, "DEPOSIT", initial_balance)


#  adding user login details to file
    with open(users_file, 'a') as file:
        file.write(f"{account_number},{username},{password}\n")

    print(f"✅ Customer Created Successfully! Account Number: {account_number}")

# finding a customer using account number
def find_customer(account_number):
    return customers_dict.get(account_number)

# updating balance and saving that to file 
def update_balance(account_number, new_balance):
    if account_number in customers_dict:
        customers_dict[account_number]['balance'] = new_balance
        save_customers()

# recording a transaction to file
def record_transaction(account_number, transaction_type, amount):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    try:
        with open(transactions_file, 'a') as file:
            file.write(f'{account_number},{transaction_type},{amount},{timestamp}\n')

    except:
        print("Error occured")


# depositing money to account
def deposit_money(account_number):
    customer = find_customer(account_number)
    if not customer:
        print("❌ Customer Not Found")
        return

    print(f"Current Balance: {customer['balance']}")
    amount = (input("Enter deposit amount: "))

    try:
        amount = float(amount)
        if amount < 0:
            print("❌ Invalid amount")
            return
    except ValueError:
        print("❌ Invalid amount")
        return


    amount = float(amount)
    new_balance = customer['balance'] + amount
    update_balance(account_number, new_balance)
    record_transaction(account_number, "DEPOSIT", amount)
    print(f"✅ Deposit Successful. New Balance: {new_balance}")

# withdrawing money from account
def withdraw_money(account_number):
    customer = find_customer(account_number)
    if not customer:
        print("❌ Customer Not Found")
        return

    print(f"Current Balance: {customer['balance']}")
    amount = (input("Enter Withdrawal amount: "))

    try:
        amount = float(amount)
        if amount < 0:
            print("❌ Invalid amount")
            return
    except ValueError:
        print("❌ Invalid amount")
        return

    
    if float(amount) > customer['balance']:
        print("❌ Insufficient Funds")
        return

    amount = float(amount)
    new_balance = customer['balance'] - amount
    update_balance(account_number, new_balance)
    record_transaction(account_number, "WITHDRAW", amount)
    print(f"✅ Withdrawal successful! New Balance: {new_balance}")

# checking customer balance
def check_new_balance(account_number):
    customer = find_customer(account_number)
    if customer:
        print(f"Account Balance For {customer['name']}: {customer['balance']}")
    else:
        print('❌ Customer not found')

# viewing tramnsaction history for a customer
def view_history(account_number):
    print(f'Transaction history for account number: {account_number}')
    found = False
    with open(transactions_file, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if parts[0] == account_number:
                print(f"{parts[1]}: {parts[2]} on {parts[3]}")
                found = True
    if not found:
        print("❌ No transactions found.")

# transferiung money from one account to another
def transfer_money():
    print("\nMoney Transfer")
    from_acc = input("Enter source account number: ").strip()
    to_acc = input("Enter destination account number: ").strip()
    
    if from_acc == to_acc:
        print("❌ Cannot transfer to same account!")
        return
    
    from_customer = find_customer(from_acc)
    to_customer = find_customer(to_acc)
    
    if not from_customer or not to_customer:
        print("❌ One or both accounts not found!")
        return
    
    print(f"Source account balance: {from_customer['balance']}")

    amount = input("Enter transfer amount: ")

    try:
        amount = float(amount)
        if amount <= 0:
            print("❌ Invalid amount.")
            return
    except ValueError:
        print("❌ Invalid amount.")
        return
    
    if amount > from_customer['balance']:
        print("❌ Insufficient funds!")
        return
    
    # Performing transfer
    from_new_balance = from_customer['balance'] - amount
    to_new_balance = to_customer['balance'] + amount
    
    update_balance(from_acc, from_new_balance)
    update_balance(to_acc, to_new_balance)
    
    # Recording transactions
    record_transaction(from_acc, "TRANSFER_OUT", amount)
    record_transaction(to_acc, "TRANSFER_IN", amount)
    
    print(f"✅ Transfer successful! New balance: {from_new_balance}")

# updating customer info 

def update_customer():
    acc_num = input("Enter the Account Number to update: ").strip()
    customer = find_customer(acc_num)
    if not customer:
        print("❌ Customer not found!")
        return

    print(f"Current Name: {customer['name']}")
    new_name = input("Enter new name (or press Enter to keep the same): ").strip()
    if new_name:
        customer['name'] = new_name

    print(f"Current Address: {customer['address']}")
    new_address = input("Enter new address (or press Enter to keep the same): ").strip()
    if new_address:
        customer['address'] = new_address

    save_customers()

    # Updating the user.txt file for username/password if needed
    with open(users_file, 'r') as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        parts = line.strip().split(',')
        if parts[0] == acc_num:
            print(f"Current Username: {parts[1]}")
            new_username = input("Enter new username (or press Enter to keep the same): ").strip()
            if not new_username:
                new_username = parts[1]
            print(f"Current Password: {parts[2]}")
            new_password = input("Enter new password (or press Enter to keep the same): ").strip()
            if not new_password:
                new_password = parts[2]
            updated_lines.append(f"{acc_num},{new_username},{new_password}\n")
        else:
            updated_lines.append(line)

    with open(users_file, 'w') as file:
        file.writelines(updated_lines)

    print("✅ Customer information updated successfully!")

# deleting a customer 
def delete_customer():
    acc_num = input("Enter the Account Number to delete: ").strip()
    if acc_num not in customers_dict:
        print("❌ Customer not found!")
        return

    # Confirm deletion
    confirm = input(f"Are you sure you want to delete {customers_dict[acc_num]['name']}? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("❌ Deletion cancelled.")
        return

    # Remove from dictionary and save
    del customers_dict[acc_num]
    save_customers()

    # Remove from user.txt
    with open(users_file, 'r') as file:
        lines = file.readlines()
    with open(users_file, 'w') as file:
        for line in lines:
            if not line.startswith(acc_num):
                file.write(line)

    with open(transactions_file, 'r') as file:
        lines = file.readlines()
    with open(transactions_file, 'w') as file:
        for line in lines:
            parts = line.strip().split(',')
            if parts[0] != acc_num:
                file.write(line)


    print("✅ Customer deleted successfully!")

# viewing all accounts 
def view_all_accounts():
    print("\nAll Accounts\n")

    if not customers_dict:
        print("❌ No customers found.")
        return
    
    for acc_num, info in customers_dict.items():
        print(f"Account Number: {acc_num}")
        print(f"Name: {info['name']}")
        print(f"Address: {info['address']}")
        print(f"Balance: {info['balance']}")
        print("\n")

# main program starts here 
def main():
    create_users_file()
    create_customers_file()
    create_transactions_file()
    load_customers()

    while True:
        print("\nLOGIN MENU")
        print("1. Login")
        print("2. Exit Program")
        main_choice = input("Enter choice: ")

        if main_choice == '2':
            print("Goodbye 👋")
            break
        elif main_choice != '1':
            print("❌ Invalid choice!")
            continue

        role, account_number = login()
        if not role:
            continue

# admin operations
        if role == "admin":
            while True:
                admin_menu()
                choice = input("Enter your choice (1-6): ")
                if choice == '1':
                    create_customer()
                elif choice == '2':
                    acc_num = input("Enter Account Number: ")
                    deposit_money(acc_num)
                elif choice == '3':
                    acc_num = input("Enter Account Number: ")
                    withdraw_money(acc_num)
                elif choice == '4':
                    acc_num = input("Enter Account Number: ")
                    check_new_balance(acc_num)
                elif choice == '5':
                    acc_num = input("Enter Account Number: ")
                    view_history(acc_num)
                elif choice == '6':
                    transfer_money()
                elif choice == '7':
                    update_customer()
                elif choice == '8':
                    delete_customer()
                elif choice == '9':
                    view_all_accounts() 
                elif choice == '10':
                    print("Exiting admin menu")
                    break
                else:
                    print("❌ Invalid choice!")
                
# customer operations
        else:
            while True:
                customer_menu()
                choice = input("Enter your choice (1-5): ")
                if choice == '1':
                    deposit_money(account_number)
                elif choice == '2':
                    withdraw_money(account_number)
                elif choice == '3':
                    check_new_balance(account_number)
                elif choice == '4':
                    view_history(account_number)
                elif choice == '5':
                    transfer_money()
                elif choice == '6':
                    print("Exiting customer menu")
                    break
                else:
                    print("❌ Invalid choice!")

main()
