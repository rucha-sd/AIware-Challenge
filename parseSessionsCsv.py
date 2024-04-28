import csv
from collections import defaultdict

def parse_csv_to_array(csv_filename):
    # Create a dictionary to store the counts
    sessions_by_date_and_slot = defaultdict(lambda: defaultdict(list))

    # Read the CSV file
    with open(csv_filename, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = (row['date'], row['time_slot'])
            sessions_by_date_and_slot[key][row['room']].append(row['title'])

    # Now create the output array
    output_array = []
    for date_slot, rooms in sessions_by_date_and_slot.items():
        session_counts = [len(events) for events in rooms.values()]
        if len(session_counts) > 1:  # Only consider slots with parallel sessions
            print(date_slot)
            print(session_counts)
            output_array.append(session_counts)

    return output_array

# Usage example
csv_filename = 'conference_schedule.csv'
output = parse_csv_to_array(csv_filename)
print(output)
