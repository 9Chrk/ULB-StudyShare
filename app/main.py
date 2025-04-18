import display
import auth


def main():
  while True:
    choice = display.start_menu()

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
      

if __name__ == "__main__":
  main()
