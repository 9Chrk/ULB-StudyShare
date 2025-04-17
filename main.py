from getpass import getpass

print("┌─────────────────┐")
print("│ [1] Login       │")
print("│ [2] Register    │")
print("│ [3] Exit        │")
print("└─────────────────┘")

choice = input(">> ")
print()

if choice == "1":
  username = input("Username: ")
  password = getpass("Password: ")
  
  print("\nLogging in...")
  print(f"Welcome, {username}!\n")
    
elif choice == "2":
  username = input("Username: ")
  password = input("Password: ")
  
  print("\nRegistering...")
  print(f"Welcome, {username}!\n")
   
else:
  print("Goodbye!\n")
