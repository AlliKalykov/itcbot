import sqlite3


def singleton(cls):
    instances = {}
    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance


@singleton
class DatabaseConnection:
    def __init__(self) -> None:
        self.__connection = sqlite3.connect('tgbot.sqlite3', check_same_thread=False)

    # with sqlite3.connect('tgbot.sqlite3', check_same_thread=False) as conn:
        # pass
    
    # open()

    def __enter__(self):
        return self.__connection
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.__connection.close()


class FollowersDatabase:
    def __init__(self) -> None:
        self.db = DatabaseConnection()

    def create_table_followers(self):
        with self.db as connection:
            cursor = connection.cursor()
            cursor.execute(
                '''
                    CREATE TABLE IF NOT EXISTS followers
                        (
                            id INTEGER PRIMARY KEY,
                            user_id INTEGER UNIQUE,
                            first_name TEXT,
                            last_name TEXT,
                            username TEXT
                        )
                '''
            )

    def add_follower(self, user_id : int, first_name : str, last_name : str, username : str) -> int:
        with self.db as connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    '''
                        INSERT INTO followers(user_id, first_name, last_name, username)
                        VALUES (?, ?, ?, ?)
                    ''',
                    (user_id, first_name, last_name, username)
                )
                connection.commit()
                return True
            except sqlite3.IntegrityError:
                return False
    

    def get_all_followers(self):
        with self.db as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM followers')
            return cursor.fetchall()


fl = FollowersDatabase()
# fl.create_table_followers()
# print(fl.add_follower(21234, 'alli', 'alli', 'alli'))
print(fl.get_all_followers())
