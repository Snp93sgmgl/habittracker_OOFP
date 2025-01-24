import json # JSON is required because the database is to be saved in JSON format.
from datetime import datetime, timedelta # This imports the two classes datetime and timedelta (for time differences)
import questionary # I chose questionary because I think it's the most intuitive to use once I've got to grips with fire and click.
import os # This package is used to display the workspace and to change it if necessary.

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

# Function to save the database file
def save_database(database):
    """
    This function saves the habits in the database. To do this, it is necessary to open the database in write mode so that changes can be made to it.
    A json file is only created when the first habit is added.
    """
    with open(habit_database, "w") as file_with_database: # “w”, as the file should be opened in write mode at this point.
        json.dump(database, file_with_database, indent=1) # Ensures that an indentation of one space takes place.
        # This indentation makes the JSON file easier for people to read.

# Function to create a Habit and assign the characteristics of a Habit
def create_a_habit(database):
    """
    This function can be used to add new habits to the database. 
    Furthermore, the ID for identifying and addressing the individual habits is assigned in this function.
    Each habit should be assigned a name, a duration and a repetition interval. 
    The repetition intervals available for selection are:
    - Daily
    - Weekly
    - Monthly
    """
    name = questionary.text("Enter the name of the habit:").ask() # Once again, questionary is used to query the user's input.
    duration_in_days = int(questionary.text("Enter the duration (in days) until the deadline (enter 0 if the habit still needs to be completed today):").ask()) 
    frequency_choice = questionary.select(
        "Choose the frequency of the habit:",
        choices=["Daily", "Weekly", "Monthly"] # 3 frequency intervals should be predefined
    ).ask()
    
    habit = Habit(name, duration_in_days, frequency_choice) # here the blueprint that was created in the class is transferred to an object
    
    # I need a system that ensures that my Habit ID does not appear more than once. With the following If condition, 
    # I always get an ID that is larger than the largest in the system so far (it would be better to fill in any gaps in the ID 
    # list caused by deleted habits, but I have not found a solution for this yet).
    # This also ensures that an error does not occur if the list is empty (i.e. if the first habit is entered).
    if database["habits"]:
        last_habit = database["habits"][-1]
        last_habit_id = last_habit["id"]
        habit.id = last_habit_id + 1
    else:
        habit.id = 1

    habit.start = datetime.now().strftime('%Y-%m-%d') # Change the format again, JSON cannot save the output of the datetime package directly.
    database["habits"].append(habit.to_dict()) # Adds the habit to the database. Since the to_dict method is used, it is converted into a dictionary.
    save_database(database) # The change (i.e. the new habit) is saved in the database file

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
        date_today = datetime.now().strftime('%Y-%m-%d')
        if habit.deadline < date_today and habit.completed == False: # If the deadline is less than today's date and the habit is not yet marked as completed, it should receive the status outdated.
            habit.timeout = True
        else:
            habit.timeout = False
        completed_status = "Yes" if habit.completed else "No" # At this point, a ternary operator is used to write the if-else condition in just one line.
        outdated_status = "Yes" if habit.timeout else "No" # Same procedure here.
        completed_date = habit.completed_date

        # I use f-strings because they are a very efficient way to integrate variables into strings.
        print(f"ID: {habit.id}, Name: {habit.name}, Start: {habit.start}, Deadline: {habit.deadline}, Outdated: {outdated_status}, "
              f"Frequency: {habit.frequency}, Completed: {completed_status}, Completed on: {completed_date}")


# I have decided to write the requirements for the analysis of existing habits in different functions in order to keep the individual functions clearer.

# This function returns an enumeration of all habits with the same periodicity
def show_same_freq_habits(database):
    """
    This function lists all habits in the database that have the same repetition interval. 
    First you must select the interval for which the habits are to be output (daily, weekly or monthly), 
    then the following values are output from the database:
    - The ID of the habit
    - The name of the habit
    - The date when the habit was registered
    - The deadline by which the habit must be completed if it is not to be considered failed
    - The frequency, i.e. the repetition interval
    - The status of the habit, which provides information on whether the habit has already been completed.
    """
    if not database["habits"]: # This checks whether the dictionary is empty
        print("There are no habits yet.")
        return # To exit the function so that the rest of the code is not executed if the dictionary is empty
    choice = questionary.select( # At this point, a user query is made using the CLI questionary to find out how often this habit should be repeated
            "The habits of which repetition interval should be displayed?:",
            choices=["Daily", "Weekly", "Monthly"] # 
        ).ask()
    
    for habit_data in database["habits"]:
        habit = Habit.from_dict(habit_data) # The specific habit is again loaded into the habit variable via a query of the class object
        
        if habit.frequency == choice:  # Only show habits that match the chosen frequency
            completed_status = "Yes" if habit.completed else "No"  
            print(f"ID: {habit.id}, Name: {habit.name}, Start: {habit.start}, Deadline: {habit.deadline}, "
                  f"Frequency: {habit.frequency}, Completed: {completed_status}")


# Function to mark a habit as completed
# This means that the value for the completed entry is set to True. In addition, the placeholder value of the entry “completed_date” (None) 
# is overwritten with the calendar date of the day on which the habit was entered as completed.
def mark_habit_as_completed(database, habit_id):
    """
    This function marks a habit as completed. 
    The calendar day on which the habit was marked as completed is also entered.
    """
    habit_data = next((habits for habits in database["habits"] if habits["id"] == habit_id), None) # Here, next() is used to iterate through the habit database until the corresponding ID is found.
    if habit_data:
        habit = Habit.from_dict(habit_data)
        habit.mark_completed()
        habit_data["completed"] = True  # Updates the habit status entry in the database
        habit_data["completed_date"] = datetime.now().strftime('%Y-%m-%d') # Change the format, JSON cannot save the output of the datetime package directly.
        save_database(database)
        print(f"Habit '{habit.name}' has been marked as completed")
    else:
        print(f"No habit found with ID {habit_id}") # If the ID could not be found, this response is displayed.


# Function to check which habits are still to be completed today, as their deadline expires today
def check_for_urgent_habits(database):
    """
    This function is used to check whether a habit is about to expire on the day of the query.
    This function allows the user to be notified of urgent matters so that they can deal with them in good time.
    habits that are already marked as completed are not displayed as they are no longer urgent.
    """
    today = datetime.now().strftime('%Y-%m-%d') # The date is formatted again in the format YYYY-MM-DD
    deadline_count = 1 # Sets the start value for the loop to 1.
    for habit_data in database["habits"]:
        habit = Habit.from_dict(habit_data)
        if habit.deadline == today and not habit.completed: # This is where you can see whether a habit has already been completed
            print(f"Habit '{habit.name}' is still to be completed today and has not yet been completed!")
            deadline_count = 0
    
    # With the second if condition in this function, I can prevent the message “There are no habits for today whose deadline also expires today” 
    # from appearing as often as there are habits. If no habit expires today, it is sufficient to output this value once.
    # This would happen if the output of this message also took place in the for loop.
    if deadline_count == 1:
            print("There are no habits for today whose deadline also expires today")


# This function allows the user to delete a habit from the database (e.g. because it is outdated or should no longer be tracked). 
# As with the function for marking the habit as completed, the habit is deleted via the ID value assigned to it.
def delete_habit(database, habit_id):
    """
    This function allows the user to delete a habit. The user is asked which ID the habit to be deleted has. 
    The corresponding habit is then deleted. If there is no habit with the corresponding ID, the user is notified of this.
    """
    habit_data = next((habits for habits in database["habits"] if habits["id"] == habit_id), None) # Here, next() is used to iterate through the habit database until the corresponding ID is found.
    if habit_data:                                                                                 # Just like the function for marking habits as completed.
        habit = Habit.from_dict(habit_data)
        database["habits"] = [habit for habit in database["habits"] if habit["id"] != habit_id]
        save_database(database) # The change (the deletion of the habit) is written to the database file
        print(f"Habit '{habit.name}' has been deleted")
    else:
        print(f"No habit found with ID {habit_id}") # If the ID could not be found, this response is displayed.


def change_working_directory():
    """
    This function is intended to check the current working directory, if necessary, adjust it according to the user's wishes.
    If the directory specified by the user does not exist or the user does not have the authorization to view it, he will receive a corresponding error message.
    """
    # Displays the current working directory
    current_working_directory = os.getcwd()
    print(f"Current working directory: {current_working_directory}")

    # Asks the user whether the directory should be retained
    keep_working_directory = questionary.confirm(
        f"Do you want to keep the current working directory?"
    ).ask()

    # If the directory is not to be retained, the user should be asked for a new directory
    if not keep_working_directory:
        new_working_directory = questionary.text(
            "Specify the new working directory in which the database is to be saved (e.g. C:/Users/YourUser/ExampleDirectory):"
        ).ask()

        # The directory is now to be changed. I have covered the usual error scenarios with exception handling to prevent the program from crashing.
        try:
            os.chdir(new_working_directory) # Attempts to adapt the working directory to the user's specification
            print(f"The working directory has been successfully changed. The new directory is now: {new_working_directory}") # The feedback from the interpreter when the change has worked.
        except FileNotFoundError:
            print(f"Error: The specified directory '{new_working_directory}' does not exist.") # If the directory does not exist, this error is displayed
        except PermissionError:
            print(f"Error: You do not have permission to change to the directory '{new_working_directory}'.") # If the user does not have the necessary authorizations to view the selected directory
    else:
        print("The working directory remains unchanged.")


# A function to output the longest habit run series ever. Here the user can display his greatest success.

def longest_streak_overall(database):
    """
    This function calculates the longest streak of a consecutive completed habit overall.
    A streak is a sequence of successful consecutive completions of a habit.
    """
    if not database["habits"]:  # The following message should be displayed if no habits are available.
        print("There are no habits yet.")
        return

    # Group habits by their name
    habits_by_name = {} # An empty dictionary is to be created here
    for habit_data in database["habits"]: # Iteration through the list with habits
        habit = Habit.from_dict(habit_data) # Habits are loaded into the “habit” variable
        # 
        if habit.completed_date:  
            if habit.name not in habits_by_name:
                habits_by_name[habit.name] = []
            habits_by_name[habit.name].append(habit)

    # Now, check for streaks
    longest_streak = 0
    streak_habit_name = ""
    
    for habit_name, habits in habits_by_name.items():
        # Sort the habits by date of completion (the date must have the format YYYY-MM-DD)
        habits.sort(key=lambda h: h.completed_date)

        current_streak = 1
        max_streak_for_this_habit = 1
        
        # Compare the completion dates to find streaks
        for i in range(1, len(habits)):
            previous_habit = habits[i - 1]
            current_habit = habits[i]
            # Check if the current habit was completed the day after the previous one
            previous_completed_date = datetime.strptime(previous_habit.completed_date, '%Y-%m-%d') # strptime() is the opposite of strftime. It converts strings to datetime objects.
            current_completed_date = datetime.strptime(current_habit.completed_date, '%Y-%m-%d') # It is important that the date string is formatted correctly.
            # If the if condition is True, the streak is incremented by 1, if not, the value is reset to 1
            if (current_completed_date - previous_completed_date).days == 1:
                current_streak += 1
            else:
                max_streak_for_this_habit = max(max_streak_for_this_habit, current_streak)
                current_streak = 1  # streak counter is reset

        # Ensure the last streak is checked
        max_streak_for_this_habit = max(max_streak_for_this_habit, current_streak)

        # Track the longest streak across all habits
        if max_streak_for_this_habit > longest_streak:
            longest_streak = max_streak_for_this_habit
            streak_habit_name = habit_name

    # The condition is set so that a streak is only recognized as such if at least 2 successfully completed habits have taken place in succession. 
    # Only one in succession is not yet a streak.
    if longest_streak > 1:
        print(f"The longest streak is {longest_streak} days for the habit '{streak_habit_name}'.")
    else:
        print("There are no streaks of consecutive completed habits.")


# This function can be called up by the user to obtain help (in the form of the function's docstring) 
# either via this function itself or via all other functions in the main menu.
def help_and_explanations():
    """
    In this function, the user can call up the docstring for each function of the main menu in order to obtain help 
    and understand the use of the habit tracker (i.e. the program flow).
    """
    # The CLI created by questionary is used to query which function the user would like help with.
    choice = questionary.select(
        "For which of the functions in the main menu do you need help?",
        choices=["Help and functional explanations",
                 "Add new habit", 
                 "Show all habits", 
                 "Show me all habits with the same repetition interval",    
                 "Show me the longest running streak overall",
                 "Mark habit as completed", 
                 "Check urgent habits", 
                 "Delete a habit",
                 "Change working directory", 
                 "Exit the program"]
    ).ask()

    if choice == "Help and functional explanations":
        help(help_and_explanations)
    elif choice == "Add new habit":
        help(create_a_habit)
    elif choice == "Show all habits":
        help(show_habits)
    elif choice == "Show me all habits with the same repetition interval":
        help(show_same_freq_habits)
    elif choice == "Show me the longest running streak overall":
        help(longest_streak_overall)
    elif choice == "Mark habit as completed":
        help(mark_habit_as_completed)
    elif choice == "Check urgent habits":
        help(check_for_urgent_habits)
    elif choice == "Delete a habit":
        help(delete_habit)
    elif choice == "Change working directory":
        help(change_working_directory)
    # As the exit option does not contain a function of its own, but ends the loop that is responsible for the actual 
    # program flow using “break”, a text with the explanation is simply output at this point.
    elif choice == "Exit the program": 
        print("""
              This option ends the program. 
              The previously saved habits are retained as they are saved in a JSON database with the name “habit_db.json”. 
              They can therefore be used again the next time the habit tracker is called.
              """)


# The main menu with which the user interacts is created at this point.
def main_menu(database):
    """
    This function creates the menu with which the user can interact. This function creates a menu with the following entries:
    - Add new habit
    - Show all habits
    - Show me all habits with the same repetition interval
    - Show me the longest running streak overall
    - Mark habit as completed
    - Check urgent habits
    - Delete a habit from the database
    - Change working directory
    - Exit the program
    """
    # The actual main menu is created here. 
    # The user is shown this at the start of the program after entering the name
    # of the json database file that is to be used for the Habit tracker session.
    # while true is practically an infinite loop here, as there is no condition in the loop that would somehow set the check value to false. 
    # Only the break, which is recognized by the interpreter when the user ends the program with the corresponding entry, causes the loop to be aborted.
    while True:                                  
        choice = questionary.select(             
            "What would you like to do?",        # Here are the individual entries in the main menu
            choices=["Help and functional explanations",
                     "Add new habit", 
                     "Show all habits", 
                     "Show me all habits with the same repetition interval",    
                     "Show me the longest running streak overall",
                     "Mark habit as completed", 
                     "Check urgent habits", 
                     "Delete a habit",
                     "Change working directory", 
                     "Exit the program"]
        ).ask()
        
        # This if condition query checks which selection the user has made. 
        # The entry that is identical to the user's selection is then selected and the function stored in it is executed.
        if choice == "Help and functional explanations":
            help_and_explanations()
        elif choice == "Add new habit":   
            create_a_habit(database)
        elif choice == "Show all habits":
            show_habits(database)
        elif choice == "Show me all habits with the same repetition interval":
            show_same_freq_habits(database)
        elif choice == "Show me the longest running streak overall":
            longest_streak_overall(database)
        elif choice == "Mark habit as completed": # In this part of the If-elif condition a user input is requested again.
            habit_id = int(questionary.text("Enter the ID of the habit you want to mark as completed:").ask()) # The user enters the ID of the habit that is to be marked as completed.
            mark_habit_as_completed(database, habit_id)
        elif choice == "Check urgent habits":
            check_for_urgent_habits(database)
        elif choice == "Delete a habit":
            habit_id = int(questionary.text("Enter the ID of the habit you want to delete:").ask()) # # The user enters the ID of the habit that is to be deleted
            delete_habit(database, habit_id)
        elif choice == "Change working directory":
            change_working_directory()
        elif choice == "Exit the program":
            print("The habit tracker is terminated")
            break # This break at the end of the condition for ending the program is necessary so that the program terminates when the user selects the corresponding menu entry.

# This is the first time something is executed directly. This starts the actual program, as so far only the class for the habits, 
# their methods and the functions that were created outside the class have been defined.
if __name__ == "__main__": # Since the script should be started directly and not imported
    database = load_database() # Is always executed so that the database is loaded at the beginning

    # The main menu is executed at this point. It is also executed each time the program is started. 
    main_menu(database)

