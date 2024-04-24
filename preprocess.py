import csv
from collections import defaultdict
from datetime import datetime

durationArray = []
papers_dict = {}

def parse_time(time_str):
    return datetime.strptime(time_str, '%a %d %b %Y %H:%M')

def check_overlap(session1, session2):
    # Check if two sessions overlap in time
    return session1['session_start'] < session2['session_end'] and session1['session_end'] > session2['session_start']

def mergeIntervals(time_slots):
    sorted_time_slots = sorted(time_slots.items(), key=lambda x: x[0][0])

    # Step 2: Merge overlapping intervals
    merged_slots = []
    current_start, current_end, current_rooms = None, None, defaultdict(int)

    for (start, end), rooms in sorted_time_slots:
        #start = parse_timee(start)
        #end = parse_timee(end)

        if current_start is not None and start < current_end:  # Overlap detected
            # Extend the current end time if necessary
            current_end = max(current_end, end)
            # Aggregate room counts
            for room, count in rooms.items():
                current_rooms[room] += count
        else:
            if current_start is not None:
                merged_slots.append(((current_start, current_end), dict(current_rooms)))
            # Reset for new slot
            current_start, current_end = start, end
            current_rooms = defaultdict(int)
            for room, count in rooms.items():
                current_rooms[room] = count

    # Don't forget to add the last processed interval
    if current_start is not None:
        merged_slots.append(((current_start, current_end), dict(current_rooms)))

    # Step 3: Format for output
    
    output = [(f"{start.strftime('%Y-%m-%d %H:%M:%S')} - {end.strftime('%Y-%m-%d %H:%M:%S')}", dict(rooms))
            for (start, end), rooms in merged_slots]

    # Print the merged output
    # print("after merge
    for (start, end), rooms in merged_slots:
        durationArray.append((end-start).seconds)
    return output

def parse_csv_to_array(csv_filename):
    sessions_by_date = defaultdict(list)

    # Read the CSV file
    with open(csv_filename, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            session_info = {
                'session_start': parse_time(str(row['date']) + " " + str(row['session_start'])),
                'session_end': parse_time(str(row['date']) + " " + str(row['session_end'])),
                'room': row['room'],
                'title': row['title'],
                'topic': row['topic'],
                'id': row['id']
            }
            # Group by date first
            sessions_by_date[row['date']].append(session_info)

    output_dict = {}
    for date, sessions in sessions_by_date.items():
        for i in range(len(sessions)):
            # key = str(sessions[i]['session_start']) + "-" + str(sessions[i]['session_end'])
            key = (sessions[i]['session_start'],sessions[i]['session_end'])
            if key in output_dict:
                val = output_dict[key]
                val2 = papers_dict[key]
                if sessions[i]['room'] in val:
                    val[sessions[i]['room']] += 1
                    val2[sessions[i]['room']].append(sessions[i]['id'])
                else:
                    val[sessions[i]['room']] = 1
                    val2[sessions[i]['room']] = [sessions[i]['id']]
                output_dict[key] = val
                papers_dict[key] = val2
            else :
                tmp = {}
                tmp[sessions[i]['room']] = 1
                tmpp = {}
                id_arr = [sessions[i]['id']]
                tmpp[sessions[i]['room']] = id_arr
                papers_dict[key] = tmpp
                output_dict[key] = tmp
    # for item in output_dict:
    #     print(output_dict[item])
    # for item in papers_dict.items():
    #     print(item)
    return output_dict

def formatMerged(intervals):
    output = [list(session_info.values()) for _, session_info in intervals]
    return output
    # Print the output
    # print(output)

def merge_overlaps(data):
    # Sort data by start time
    data = sorted(data.items(), key=lambda x: x[0][0])

    
    merged_data = []
    current_start, current_end, current_rooms = None, None, {}

    for (start, end), rooms in data:
        if current_start is not None and start < current_end:
            # There's an overlap, merge intervals
            current_end = max(current_end, end)
            # Merge room data
            for room, events in rooms.items():
                if room in current_rooms:
                    current_rooms[room].extend(events)
                else:
                    current_rooms[room] = events
        else:
            # No overlap, push the current interval to merged_data if it exists
            if current_start is not None:
                merged_data.append(((current_start, current_end), current_rooms))
            # Reset to the new interval
            current_start, current_end, current_rooms = start, end, rooms.copy()
    
    # Add the last interval to merged data
    if current_start is not None:
        merged_data.append(((current_start, current_end), current_rooms))
    
    return merged_data

def get_topics(): 
    csv_filename = 'conference_schedule_new.csv'
    with open(csv_filename, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        topic_dict = {}
        iter = 1
        for row in reader:
            if row['session_title'] not in topic_dict:
                topic_dict[row['session_title']] = iter
                iter+=1
        return topic_dict

def processor():
    # Usage example
    csv_filename = 'conference_schedule_new.csv'
    output = parse_csv_to_array(csv_filename)
    mergedOutput = formatMerged( mergeIntervals(output))
    # print("Array of merged sessions")
    # print("duration array")
    # print(durationArray)
    # print(output)
    merged_intervals = merge_overlaps(papers_dict)

    return {
        "merged_intervals": merged_intervals,
        "duration_array": durationArray,
        "merged_output": mergedOutput
    }

    # Process the data to merge overlaps
    
    # Output the merged intervals
    # for interval, rooms in merged_intervals:
    # print(f"Interval: {interval[0].strftime('%Y-%m-%d %H:%M:%S')} to {interval[1].strftime('%Y-%m-%d %H:%M:%S')}, Rooms: {rooms}")
