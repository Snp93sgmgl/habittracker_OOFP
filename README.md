# The habit-tracking app for object-oriented and functional programming with Python  

This is the readme file explaining the functions and use of the habit tracking app for the course “object-oriented and functional programming with python” 


## Files

- Dependencies that are not part of the standard Python libraries are listed in the “requirements.txt” file and can be installed directly via this file.
- The ready-made database for testing the analysis function to output the existing habits and their attributes can be found in the habits_db.json file
- The program code of the actual habit tracking app can be found in the file “habit_tracking_app.py”.
- The “test_of_analytics.py” file contains the code for testing the function that outputs the existing habits and their attributes. This code applies the function directly to the test database.
- The file “test_of_class.py” contains the code for testing the created class, which serves as a blueprint for the habits to be tracked.

## Using the habit tracker

To use the habit tracker, the file “habit_tracking_app.py” must be called in python3. The command line interface for interacting with the user starts automatically.

## Functions of the Habit Tracker

The user can choose from the following entries:
- "Help and functional explanations",
- "Add new habit"
- "Show all habits"
- "Show me all habits with the same repetition interval"
- "Show me the longest running streak overall"
- "Mark habit as completed"
- "Check urgent habits"
- "Delete a habit"
- "Change working directory"
- "Exit the program"

The “Help and functional explanations” function allows the user to display help for all entries in the main menu, including the options for the individual functions.

The user's registered habits are retained between the individual sessions of the tracker, as they are stored in a specially created database.

