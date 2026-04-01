from core.db.init import execute_sql_script
from gui.app import run


def main():
    execute_sql_script("schema.sql")
    run()


if __name__ == "__main__":
    main()
