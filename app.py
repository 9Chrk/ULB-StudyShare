import sys
from core.db_config import execute_sql_script


# Choose the UI based on command line arguments
if '--gui' in sys.argv:
    from gui.main import run
else:
    from cli.main import run


def main():
    execute_sql_script("schema.sql")
    run()

if __name__ == "__main__":
    main()
