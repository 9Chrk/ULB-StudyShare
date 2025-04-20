from getpass import getpass

def login():
  while True:
    print("-----------")
    username = input("Username : ")
    password = getpass("Password : ")
    print("-----------\n")

    print("Verifying credentials…")
    
    # Check on the database !!! ./core
    
    # simulation
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
      # Add the new user to the database !!! ./core
      print(f"✅ The account for {username} has been successfully created!\n")
      return True
    