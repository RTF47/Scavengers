import sqlitecloud
import requests

class Leaderboard:
    def __init__(self):
        # Подключение к SQLite Cloud
        self.conn = sqlitecloud.connect('sqlitecloud://ctj9mompnk.g1.sqlite.cloud:8860/leaderborad?apikey=54lnSWGBadvFIlQMFlYfr5axUaNRWujyageJIKduPTA')


    def check_connection(self):
        try:
            response = requests.get('https://www.google.com/', timeout=3)
            return True
        except requests.RequestException:
            return False


    def check_unique_name(self, name):
        cursor = self.conn.cursor()
        cursor.execute('SELECT username FROM leaderboard WHERE username = ?', (name,))
        return cursor.fetchone() is not None


    def get_user_time(self, username):
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT time FROM leaderboard WHERE username = ?',
            (username,)
        )
        row = cursor.fetchone()
        return row[0] if row else None


    def save_score(self, name, time_ms):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO leaderboard (username, time) VALUES (?, ?)', (name, time_ms))
        self.conn.commit()


    def update_score(self, name, time_ms):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE leaderboard
            SET time = ?
            WHERE username = ?
        ''', (time_ms, name))
        self.conn.commit()


    def get_top_scores(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT username, time FROM leaderboard ORDER BY time ASC LIMIT 5')
        return cursor.fetchall()