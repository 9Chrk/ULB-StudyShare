from core.db_config import execute_sql_script
from gui.main import run


def main():
    execute_sql_script("schema.sql")
    run()


if __name__ == "__main__":
    main()
