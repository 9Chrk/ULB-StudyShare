import os


def start():
    menu = r"""
    ┌──────────────┐
    │ [1] Log in   │
    │ [2] Register │
    │ [Q] Exit     │
    └──────────────┘
    """
    os.system("cls" if os.name == "nt" else "clear")
    print(menu, end="")
    choice = input(">> Select an option: ")
    print()
    return choice
