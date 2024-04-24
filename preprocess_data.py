import csv
from collections import defaultdict
from datetime import datetime
import GA
import pandas as pd

papers_dict = {}
duration_array = []

def parse_time(time_str):
    return datetime.strptime(time_str, '%a %d %b %Y %H:%M')

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
    return output_dict

def session_details(time_slots):
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
        duration_array.append((end-start).seconds/60)
    output = [list(session_info.values()) for _, session_info in output] 
    num_tracks_per_session =  [len(session) for session in output]
    return duration_array, num_tracks_per_session

def get_topics(filename): 
    csv_filename = filename
    with open(csv_filename, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        topic_dict = {}
        iter = 1
        for row in reader:
            if row['session_title'] not in topic_dict:
                topic_dict[row['session_title']] = iter
                iter+=1
        return topic_dict

def create_papers(input_file):
    papers = []
    input = pd.read_csv(input_file)
    topics_dict = get_topics(input_file)
    # print(input['duration'])
    # remove 'm' from input[duartion] and convert to int
    # input['duration'] = input['duration'].str.replace('m', '').astype(int)
    # convert author to array by separating comma separated values
    # drop row where author is blank


    # replace Nan values in author with ''
    input['author'] = input['author'].fillna('')

    input['author'] = input['author'].str.split(',')

    # print(input['author'])
    for i in range(len(input)):
        # check if author is Nan
        # if type(input['author'][i]) == float:
        #     # set as empty list
        #     input['author'][i] = []
        paper = GA.Paper(id=input['id'][i], authors=input['author'][i], duration=input['duration'][i], topic=topics_dict[input['session_title'][i]])
        papers.append(paper)
    return papers

def create_solution():
    # create session object, refer to session from GA.py
    # each session should have array tracks eg, session1 = [track1, track2] where track1 and track2 are lists of Paper objects
    # each session should have max_lenght/duration
    # create Solution object and pass sessions
    pass