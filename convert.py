import json
import csv
from datetime import datetime, timedelta

def convert_json_to_csv(json_filename, csv_filename='conference_schedule_new.csv'):
    with open(json_filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        headers = ["id","year", "date", "session_start", "session_end", "room", "chair", "session_title", "duration", "dtstart", "dtend", "location", "author", "type", "title", "topic"]
        csv_writer.writerow(headers)
        id_counter = 1
        for year, dates in data.items():
            for date, time_slots in dates.items():
                for time_slot, sessions in time_slots.items():
                    # Split the time_slot into session_start and session_end
                    if '-' in time_slot:
                        session_start, session_end = time_slot.split(' - ')
                        session_start_dt = datetime.strptime(f"{date} {session_start.strip()}", "%a %d %b %Y %H:%M")
                        session_end_dt = datetime.strptime(f"{date} {session_end.strip()}", "%a %d %b %Y %H:%M")
                    else:
                        session_start_dt = datetime.strptime(f"{date} {time_slot}", "%a %d %b %Y %H:%M")
                        session_end_dt = session_start_dt  # Assume same start and end time if not specified
                    for session in sessions:
                        print(session)
                        room = session.get("room", "")
                        chair = session.get("chair", "")
                        session_title = session.get("session_title", "").replace('\n', ' ')  # Clean newlines in session title

                        for event in session["events"]:
                            duration_minutes = event["duration"]  # Assuming the format "6m"
                            event_start_time = event['start_time']
                            dtstart = datetime.strptime(f"{date} {event_start_time}", "%a %d %b %Y %H:%M")
                            dtend = dtstart + timedelta(minutes=duration_minutes)
                            authors = ", ".join(event["authors"])

                            csv_writer.writerow([
                                id_counter,
                                year,
                                date,
                                session_start,
                                session_end,
                                room,
                                chair,
                                session_title,
                                event["duration"],
                                dtstart.strftime("%Y-%m-%dT%H:%M:%S"),
                                dtend.strftime("%Y-%m-%dT%H:%M:%S"),
                                room,  # Assuming room is used as location
                                authors,
                                event["type"],
                                event["title"],
                                event["topic"]
                            ])

                            id_counter += 1

# Usage Example
convert_json_to_csv('msr_papers_data_new.json')
