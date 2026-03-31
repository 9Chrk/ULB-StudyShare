from core import user
from getpass import getpass


def login():
    while True:
        print("-----------")
        username = input("Username : ")
        password = getpass("Password : ")
        print("-----------\n")

        print("Verifying credentials…")
        
        is_ok, message = user.check(username, password)
        if is_ok:
            print("✅ Login successful\n")
            return True

        print(f"❌ {message}\n")
        retry = input(">> Retry ? [yes/no] : ").strip().lower()
        print()
        
        if retry == "no":
            return False


def register():
    while True:
        print("-----------")
        username = input("Choose a username : ")
        email = input("Enter your email : ")
        password = getpass("Choose a password : ")
        confirm = getpass("Confirm your password : ")
        print("-----------\n")

        if password != confirm:
            print("❌ Passwords do not match.\n")
            retry = input(">> Retry ? [yes/no] : ").strip().lower()
            print()
            
            if retry == "no":
                return False
            
        else:
            is_ok, message = user.add(username, password, email)
            if is_ok:
                print(f"✅ The account for {username.strip()} has been successfully created!\n")
                return True

            print(f"❌ {message}\n")
            retry = input(">> Retry ? [yes/no] : ").strip().lower()
            print()

            if retry == "no":
                return False
