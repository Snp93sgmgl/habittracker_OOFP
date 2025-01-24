# This code is partially identical to the actual code of the app. 
# Those functions and methods of the class that are not required for testing the “show_habits()” function have been removed for the sake of clarity. 
# The test was performed by outputting the test database from the perspective of a fictitious calendar date after adding the last habit.
# The documentation in the “show_habits()” function has been adapted.

import json # JSON is required because the database is to be saved in JSON format.
from datetime import datetime, timedelta # This imports the two classes datetime and timedelta (for time differences)

# The default file name of the database is assigned
habit_database = "habits_db.json"

# Functions that are defined within classes are called methods. 
# They make sense when working directly with attributes of the class or instance.
# Here a class is defined in order to have a defined blueprint for the habits to be saved.
# At least one class is required to fulfill the requirements of the guidelines.
class Habit: # The name of the class is capitalized as is usual in python.
    def __init__(self, name, duration_in_days, frequency):
        """
        When the Habit class is called, it should request the following three values from the user:
        The name the user wants to give the habit: name
        How long the user has to complete the habit, measured in days: duration_in_days
        The repetition interval of the habit. Three frequencies should be possible: 1. daily, 2. weekly and 3. monthly: frequency
        """
        self.name = name
        self.duration_in_days = duration_in_days
        # Use the current date to calculate a difference in when the deadline is due. The date should then be formatted as a string of the form YYYY-MM-DD
        self.deadline = (datetime.now() + timedelta(days=duration_in_days)).strftime('%Y-%m-%d') # Format needs to be changed, because json is not able to deal with datetime package output.
        # strftime() converts datetime objects into strings.
        # The format is therefore adapted to the same target format everywhere so that it is uniform. 
        self.frequency = frequency
        self.completed = False # False is assigned as the default value. This value is overwritten if the habit is marked as completed by the user.
        self.id = None # ID is added later when the habit is saved. Until then, the ID is given the blank value None. The ID is used to directly identify and address a habit.
        self.start = None # The start value on which the habit was created is saved here. As with the ID, it is set to the blank value None at the start
        self.timeout = None # This value saves if a habit was not completed on time. It also receives the blank value None by default
        self.completed_date = None # Saves the day on which the habit is marked as completed. It also receives the blank value None by default



    @staticmethod ## Identifies the method from_dict as a static method. A static method does not require an instance of the class to be called. 
    # I therefore use the parameter “data” instead of “self” here.
    def from_dict(data):
        """
        Converts a dictionary into a habit object
        """
        habit = Habit(data["name"], data["duration_in_days"], data["frequency"])
        habit.deadline = data["deadline"]
        habit.completed = data["completed"]
        habit.id = data["id"]
        habit.start = data["start_date"]
        habit.timeout = data["timeout"]
        habit.completed_date = data["completed_date"]
        return habit


# Function to load the database (or create an empty database if it does not exist, i.e. if the exception applies)
def load_database():
    """
    This function is used to load the database. It checks whether a database exists. 
    If this is not the case, an empty database is created. The JSON format is used to save the habits.
    The database is only opened by this function in read mode:
    """
    try:
        with open(habit_database, "r") as file_with_database: # "r", as the file should only be opened in read mode at this point.
            return json.load(file_with_database) # In order for the content of the file to be recognized as JSON data.
    except FileNotFoundError: #  If the file does not exist, repeat exception handling so that the program doesn't crash.
        return {"habits": []} # If the file was not found, the function returns a dictionary containing the key “habits” with an empty list as value. 
    # This is a standardized return to ensure that the rest of the program can still work with a valid structure (e.g. an empty list of habits).


# Function to display all habits
def show_habits(database):
    """
    This function lists all the habits in the database. The following values are output from the database: 
    - The ID of the habit
    - The name of the habit
    - The date when the habit was registered
    - The deadline by which the habit must be completed if it is not to be considered failed
    - Whether the habit has already expired without being completed
    - The frequency, i.e. the repetition interval
    - The status of the habit, which provides information on whether the habit has already been completed.
    - Provided the habit has been completed: The date on which it was completed
    """
    if not database["habits"]: # This checks whether the dictionary is empty
        print("There are no habits yet.")
        return # To exit the function so that the rest of the code is not executed if the dictionary is empty
    for habit_data in database["habits"]:
        habit = Habit.from_dict(habit_data) # Here, the specific habit is loaded into the habit variable via a query of the class object
        test_date = "2025-03-15" # A fictitious date is used here instead of the current date in the habit Tracker app script. 
        # This means that the “show_habits()” function and its contents are tested with the habits in the test database and a date that is after the most recent habit that has been entered. 
        # This makes it possible, for example, to recognize whether a habit that was not marked as completed on time is really recognized as outdated.
        # You can also test whether all habits are displayed correctly, as was intended when the function was programmed.
        # The assignment of the habit id, i.e. that there is no duplication, can also be tested here.
        if habit.deadline < test_date and habit.completed == False: # If the deadline is less than today's date and the habit is not yet marked as completed, it should receive the status outdated.
            habit.timeout = True
        else:
            habit.timeout = False
        completed_status = "Yes" if habit.completed else "No" # At this point, a ternary operator is used to write the if-else condition in just one line.
        outdated_status = "Yes" if habit.timeout else "No" # Same procedure here.
        completed_date = habit.completed_date

        # I use f-strings because they are a very efficient way to integrate variables into strings.
        print(f"ID: {habit.id}, Name: {habit.name}, Start: {habit.start}, Deadline: {habit.deadline}, Outdated: {outdated_status}, "
              f"Frequency: {habit.frequency}, Completed: {completed_status}, Completed on: {completed_date}")


database = load_database()
show_habits(database)