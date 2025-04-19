from terminal_ui import menu
from terminal_ui import auth

def run():
  while True:
    choice = menu.start()

    if choice == "1":
      if auth.login():
        break
      
    elif choice == "2":
      if auth.register():
        break
      
    elif choice.upper() == "Q":
      print("See you soon!\n")
      break

    else:
      print("❌ Invalid option. Please try again.\n")
