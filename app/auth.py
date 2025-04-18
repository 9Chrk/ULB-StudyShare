from getpass import getpass


def login():
  while True:
    print("-----------")
    username = input("Username : ")
    password = getpass("Password : ")
    print("-----------\n")

    print("Verifying credentials…")
    
    if username == "admin" and password == "admin":
      print("✅ Login successful\n")
      return True

    print("❌ Incorrect username or password.\n")
    retry = input(">> Retry ? [yes/no] : ").strip().lower()
    print()
    
    if retry == "no":
      return False


def register():
  while True:
    print("-----------")
    username = input("Choose a username : ")
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
      print(f"✅ The account for {username} has been successfully created!\n")
      return True