from abc import ABC, abstractmethod

class DatabaseManagerInterface(ABC):
    """
    Interface for managing database connections and operations.
    """

    @abstractmethod
    def add_streak(self, activity: str, done: bool):
        """
        Add a streak entry to the database given the activity name and its completion status.
        """
        pass

    @abstractmethod
    def delete_activity(self, activity: str):
        """
        Delete all entries of a certain activity from the database.
        """
        pass

    @abstractmethod
    def get_activity_streaks(self) -> dict[dict]:
        """
        Gets the streaks of all activities in the database.
        Returns a dictionary where the keys are activity names and the values are dictionaries.
        Each activity dictionary contains the keys "is_done_today" and "most_recent_streak".
        """
        pass