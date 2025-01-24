# In this test, I have adopted the class that represents the blueprint of my habits. 
# I then used the “assert” statement to check whether the exemplary inputs that 
# I had specified were actually made in the way that I had imagined during programming.


from datetime import datetime, timedelta

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

# A method with which the habit is defined as completed
    def mark_completed(self):
        """
        Marks the habit as completed and records the completion date.
        """
        self.completed = True
        self.completed_date = datetime.now().strftime('%Y-%m-%d') # Change the format, JSON cannot save the output of the datetime package directly.
    

# I decided to use the dictionary data type to store the habits. 
# This was done in view of the fact that json has difficulties with data types that are specific to some packages (such as datetime objects)
# Moreover, this happened because I need an unordered data type and the assignment of key-value pairs is very convenient for me at this point.
    def to_dict(self):
        """
        Converts the habit object into a dictionary that is later saved in a file.
        """
        return {
            "id": self.id,
            "name": self.name,
            "start_date": self.start,
            "duration_in_days": self.duration_in_days,
            "deadline": self.deadline,
            "frequency": self.frequency,
            "completed": self.completed,
            "timeout": self.timeout,
            "completed_date": self.completed_date
        }

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
    

# Unit Test Suite

def test_create_habit_class():
    habit = Habit("Joggen", 30, "daily")
    assert habit.name == "Joggen", f"Expected 'Joggen', but got {habit.name}"
    assert habit.duration_in_days == 30, f"Expected 30, but got {habit.duration_in_days}"
    assert habit.frequency == "daily", f"Expected 'daily', but got {habit.frequency}"
    assert habit.completed == False, f"Expected False, but got {habit.completed}"
    print("test_create_habit_class passed.")

def test_mark_completed():
    habit = Habit("Lesen", 15, "daily")
    habit.mark_completed()
    assert habit.completed == True, f"Expected True, but got {habit.completed}"
    assert habit.completed_date is not None, f"Expected completed_date to be set, but got {habit.completed_date}"
    print("test_mark_completed passed.")

def test_to_dict():
    habit = Habit("Kochen", 7, "weekly")
    habit_dict = habit.to_dict()
    assert habit_dict["name"] == "Kochen", f"Expected 'Kochen', but got {habit_dict['name']}"
    assert habit_dict["duration_in_days"] == 7, f"Expected 7, but got {habit_dict['duration_in_days']}"
    assert habit_dict["completed"] == False, f"Expected False, but got {habit_dict['completed']}"
    print("test_to_dict passed.")

def test_from_dict():
    habit_data = {
        "id": None,
        "name": "Yoga",
        "start_date": None,
        "duration_in_days": 20,
        "deadline": "2025-02-15",
        "frequency": "daily",
        "completed": False,
        "timeout": None,
        "completed_date": None
    }
    habit = Habit.from_dict(habit_data)
    assert habit.name == "Yoga", f"Expected 'Yoga', but got {habit.name}"
    assert habit.duration_in_days == 20, f"Expected 20, but got {habit.duration_in_days}"
    assert habit.deadline == "2025-02-15", f"Expected '2025-02-15', but got {habit.deadline}"
    assert habit.completed == False, f"Expected False, but got {habit.completed}"
    print("test_from_dict passed.")


# A function is created that executes all tests in sequence.
def run_tests():
    test_create_habit_class()
    test_mark_completed()
    test_to_dict()
    test_from_dict()

# Run all tests
run_tests()
