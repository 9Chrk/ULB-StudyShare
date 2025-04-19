import sys

if '--gui' in sys.argv:
  from gui.main import run
else:
  from terminal_ui.main import run

run()
