def start():
  menu = r"""
  ┌──────────────┐
  │ [1] Log in   │
  │ [2] Register │
  │ [Q] Exit     │
  └──────────────┘
  """
  print(menu, end="")
  choice = input(">> Select an option: ")
  print()
  return choice
  