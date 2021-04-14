import sqlite3
import json
from models import Entry

ENTRIES = []

def get_all_entries():
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.date,
            a.text,
            a.concept,
            a.moodId
        FROM entries a
        """)

        # Initialize an empty list to hold all entry representations
        entries = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an entry instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Entry class above.
            entry = Entry(row['id'], row['date'], row['text'],
                            row['concept'], row['moodId'])

            entries.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entries)

def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.date,
            a.text,
            a.concept,
            a.moodId
        FROM entries a
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an entry instance from the current row
        entry = Entry(data['id'], data['date'], data['text'],
                            data['concept'], data['moodId'])

        return json.dumps(entry.__dict__)

def create_entry(entry):
    # Get the id value of the last entry in the list
    max_id = ENTRIES[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the entry dictionary
    entry["id"] = new_id

    # Add the entry dictionary to the list
    ENTRIES.append(entry)

    # Return the dictionary with `id` property added
    return entry


def delete_entry(id):
    # Initial -1 value for entry index, in case one isn't found
    entry_index = -1

    # Iterate the ENTRIES list, but use enumerate() so that you
    # can access the index value of each item
    for index, entry in enumerate(ENTRIES):
        if entry["id"] == id:
            # Found the entry. Store the current index.
            entry_index = index

    # If the entry was found, use pop(int) to remove it from list
    if entry_index >= 0:
        ENTRIES.pop(entry_index)



def update_entry(id, new_entry):
    # Iterate the ENTRIES list, but use enumerate() so that
    # you can access the index value of each item.
    for index, entry in enumerate(ENTRIES):
        if entry["id"] == id:
            # Found the entry. Update the value.
            ENTRIES[index] = new_entry
            break