import sqlite3
from collections import defaultdict
from datetime import datetime, timedelta


class DatabaseManager:
    def __init__(self):
        self.cursor = self._initialize_database()

    @staticmethod
    def _initialize_database(db_name='streak_tracker.db'):
        # Connect to the database (or create it if it doesn't exist)
        conn = sqlite3.connect(db_name, check_same_thread=False)

        # Create a cursor object
        cursor = conn.cursor()

        # Create the table with a unique constraint on Timestamp and activity
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS streaks (
            Timestamp TEXT NOT NULL,
            activity TEXT NOT NULL,
            done BOOLEAN NOT NULL,
            UNIQUE(Timestamp, activity)
        )
        ''')

        # Commit the changes
        conn.commit()
        return cursor

    def close_connection(self):
        # Close the database connection
        self.cursor.connection.close()

    @staticmethod
    def get_current_time_iso():
        return datetime.now().date().isoformat()

    def add_streak(self, activity, done):
        timestamp = self.get_current_time_iso()

        # Insert or replace a streak into the database
        self.cursor.execute('''
        INSERT OR REPLACE INTO streaks (Timestamp, activity, done)
        VALUES (?, ?, ?)
        ''', (timestamp, activity, done))

        # Commit the changes
        self.cursor.connection.commit()

    def _get_most_recent_streak(self, activity):
        # Query to get all streaks for the given activity, ordered by Timestamp
        self.cursor.execute('''
        SELECT Timestamp, done FROM streaks
        WHERE activity = ?
        ORDER BY Timestamp DESC
        ''', (activity,))

        rows = self.cursor.fetchall()
        if not rows:
            return 0

        # Calculate the most recent streak
        most_recent_streak = 0
        current_streak = 0
        previous_date = None

        for row in rows:
            timestamp, done = row
            date = datetime.strptime(timestamp, '%Y-%m-%d').date()

            if done:
                if previous_date is None or date == previous_date - timedelta(days=1):
                    current_streak += 1
                else:
                    break
                previous_date = date
            else:
                break

        most_recent_streak = max(most_recent_streak, current_streak)
        return most_recent_streak

    def _get_all_activities(self):
        # Query to get all distinct activities
        self.cursor.execute('''
        SELECT DISTINCT activity FROM streaks
        ''')

        activities = [row[0] for row in self.cursor.fetchall()]
        return activities

    def delete_activity(self, activity):
        # Delete all entries of a certain activity from the database
        self.cursor.execute('''
        DELETE FROM streaks WHERE activity = ?
        ''', (activity,))

        # Commit the changes
        self.cursor.connection.commit()

    def is_activity_done_today(self, activity):
        # Get today's date in ISO format
        today = self.get_current_time_iso()

        # Query to check if the activity is done today
        self.cursor.execute('''
        SELECT done FROM streaks
        WHERE activity = ? AND Timestamp = ?
        ''', (activity, today))

        row = self.cursor.fetchone()
        return row is not None and row[0] == 1

    def get_activity_streaks(self) -> dict:
        activities = self._get_all_activities()
        streak_map = defaultdict(dict)
        for activity in activities:
            content = {}
            is_done_today = self.is_activity_done_today(activity)
            content["is_done_today"] = is_done_today
            content["most_recent_streak"] = self._get_most_recent_streak(activity)
            streak_map[activity] = content
        print(streak_map)
        return streak_map



if __name__ == "__main__":
    db_manager = DatabaseManager()
