import time
import json
import os

print("--WELCOME TO ZERA BANK--")
choice = input("Create New Bank Profile or Login (create/login): ")

if choice.lower() == "create":
    user_name = input("Enter your name: ")
    user_pin = input("Enter your PIN: ")

    # Define the absolute file path for the database.json file
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.json")

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    if user_name not in data:
        print(f"Adding {user_name} to the bank database, please wait...")
        time.sleep(5)
        print(f"Added {user_name}. Proceed to exit.")
        data[user_name] = {"pin": user_pin, "salary": 0}

        # Save the updated data to the file
        with open(file_path, 'w') as file:
            json.dump(data, file)
    else:
        print(f"{user_name} already exists in the bank database.")

elif choice.lower() == "login":
    user_name = input("Enter your name: ")
    user_pin = input("Enter your PIN: ")

    # Define the absolute file path for the database.json file
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.json")

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    if user_name in data and data[user_name]["pin"] == user_pin:
        print(f"Welcome back, {user_name}!")

        # Main banking operations
        while True:
            print("\n-- BANKING OPTIONS --")
            print("1. Withdrawal")
            print("2. Deposit")
            print("3. Close Account")
            print("4. Change PIN")
            print("5. Check Deposited Money")
            print("6. Exit")
            choice = input("Enter your choice (1-6): ")

            if choice == "1":
                amount = float(input("Enter the withdrawal amount: "))
                if amount > data[user_name]["salary"]:
                    print("Insufficient balance.")
                else:
                    data[user_name]["salary"] -= amount
                    print("Withdrawal successful.")
                    print(f"New amount: {data[user_name]['salary']}")

            elif choice == "2":
                amount = float(input("Enter the deposit amount: "))
                data[user_name]["salary"] += amount
                print("Deposit successful.")

            elif choice == "3":
                confirmation = input("Are you sure you want to close your account? (y/n): ")
                if confirmation.lower() in ["y", "yes"]:
                    del data[user_name]
                    print("Account closed.")
                    break

            elif choice == "4":
                new_pin = input("Enter your new PIN: ")
                data[user_name]["pin"] = new_pin
                print("PIN changed successfully.")

            elif choice == "5":
                print(f"Deposited money: {data[user_name]['salary']}")

            elif choice == "6":
                break

            else:
                print("Invalid choice. Please try again.")

            # Log user move
            log_data = {
                "timestamp": time.time(),
                "user_name": user_name,
                "action": choice
            }
            log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs.txt")
            with open(log_file_path, "a") as log_file:
                log_file.write(json.dumps(log_data) + "\n")

        # Save the updated data to the file
        with open(file_path, 'w') as file:
            json.dump(data, file)

    else:
        print("Invalid credentials. Exiting...")

else:
    print("Invalid choice. Exiting...")
