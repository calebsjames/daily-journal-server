import sqlite3
import json
from models import Mood

def get_all_moods():
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.mood
        FROM moods a
        """)

        # Initialize an empty list to hold all mood representations
        moods = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an mood instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Mood class above.
            mood = Mood(row['id'], row['mood'])

            moods.append(mood.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(moods)

def get_single_mood(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.mood
        FROM moods a
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an mood instance from the current row
        mood = Mood(data['id'], data['mood'])

        return json.dumps(mood.__dict__)

def create_mood(mood):
    # Get the id value of the last mood in the list
    max_id = MOODS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the mood dictionary
    mood["id"] = new_id

    # Add the mood dictionary to the list
    MOODS.append(mood)

    # Return the dictionary with `id` property added
    return mood


def delete_mood(id):
    # Initial -1 value for mood index, in case one isn't found
    mood_index = -1

    # Iterate the MOODS list, but use enumerate() so that you
    # can access the index value of each item
    for index, mood in enumerate(MOODS):
        if mood["id"] == id:
            # Found the mood. Store the current index.
            mood_index = index

    # If the mood was found, use pop(int) to remove it from list
    if mood_index >= 0:
        MOODS.pop(mood_index)



def update_mood(id, new_mood):
    # Iterate the MOODS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, mood in enumerate(MOODS):
        if mood["id"] == id:
            # Found the mood. Update the value.
            MOODS[index] = new_mood
            break