import psycopg2


class Leaderboard:
    def __init__(self):
        # Подключаемся к БД
        self.conn = None
        self.connected = False
        self._connect()

    def _connect(self):
        """Подключение к PostgreSQL"""
        try:
            self.conn = psycopg2.connect(
                host="83.166.237.18",
                database="leaderboard",
                user="game_user",
                password="password"
            )
            self.connected = True
        except Exception as e:
            print(f"Ошибка подключения к БД: {e}")
            self.connected = False

    def check_connection(self):
        """Проверяем соединение с БД"""
        if not self.connected:
            self._connect()
        return self.connected

    def get_user_time(self, username):
        """Получаем время пользователя из БД"""
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT time_ms FROM players 
                    WHERE username = %s
                """, (username,))
                result = cur.fetchone()
                return result[0] if result else 0
        except Exception as e:
            print(f"Ошибка получения данных: {e}")

    def get_top_scores(self):
        """Получаем топ-5 игроков"""
        if not self.connected:
            return []

        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT username, time_ms FROM players 
                    ORDER BY time_ms ASC LIMIT 5
                """)
                return cur.fetchall()
        except Exception as e:
            print(f"Ошибка получения топа: {e}")
            return []

    def save_score(self, username, time_ms):
        """Сохраняем игрока в БД"""
        if not self.connected:
            return False

        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO players (username, time_ms)
                    VALUES (%s, %s)
                    ON CONFLICT (username) DO NOTHING
                """, (username, time_ms))
                self.conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            return False

    def update_score(self, username, time_ms):
        """Обновляем рекорд игрока"""
        if not self.connected:
            return False

        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO players (username, time_ms)
                    VALUES (%s, %s)
                    ON CONFLICT (username) DO UPDATE
                    SET time_ms = LEAST(players.time_ms, EXCLUDED.time_ms)
                """, (username, time_ms))
                self.conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка обновления: {e}")
            return False

    def check_unique_name(self, username):
        """Проверяем уникальность имени"""
        if not self.connected:
            return False

        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT EXISTS(SELECT 1 FROM players WHERE username = %s)
                """, (username,))
                result = cur.fetchone()
                return result[0] if result else False
        except Exception as e:
            print(f"Ошибка проверки имени: {e}")
            return False