from bs4 import BeautifulSoup
import requests
from pprint import pprint
import json

def get_msr_papers_by_year(year):
    conference_program = {}

    url =  f'https://conf.researchr.org/program/msr-{year}/program-msr-{year}/Detailed-Table'
    print(url)
    response = requests.get(url)
    if response.status_code != 200:
        print("NONE")
        return conference_program

    soup = BeautifulSoup(response.content, 'html.parser')
    session_tables = soup.find_all('table', class_='session-table')

    for table in session_tables:
        session_date = table['data-facet-date']
        room_name = table['data-facet-room']
        session_slot = table.find('div', class_='slot-label').text if table.find('div', class_='slot-label') else "No slot info"

        # Initialize the nested structure if not already done
        if session_date not in conference_program:
            conference_program[session_date] = {}
        if session_slot not in conference_program[session_date]:
            conference_program[session_date][session_slot] = []
        
        session_topic = table.find('div', class_='session-info-in-table')
        # text = session_topic.get_text() if session_topic else 'Text not found'
        text = session_topic.contents[0].strip() if session_topic else 'Text not found'

        chair = 'No Chair'
        small_tags = soup.find_all('small')
        for small in small_tags:
            if 'Chair(s):' in small.text:
                chair = small.text.strip()

        session_info = {
            "room": room_name,
            "chair": chair,
            "session_title": text,
            "events": []
        }
        
        # Extract each event within the session
        events = table.find_all('tr', class_='hidable')
        for event in events:
            start_time = event.find('div', class_='start-time').text if event.find('div', class_='start-time') else "Not specified"
            event_duration = event.find('strong').text if event.find('strong') else "Duration not specified"
            event_type = event.find('div', class_='event-type').text if event.find('div', class_='event-type') else "Type not specified"
            title = "No title"
            authors = [a.text for a in event.find_all('a', class_='navigate')]
            topic = event.find('div', class_='prog-track').text if event.find('div', class_='prog-track') else "Not specified"
            table_data = event.find_all('td')
            for td in table_data:
                strong_tag = td.find('strong')
                if strong_tag:
                    a_tag = strong_tag.find('a')
                    if a_tag:
                        title = a_tag.text.strip()
            event_info = {
                "authors": authors,
                "duration": float(event_duration[:-1]),
                "start_time": start_time,
                "title": title,
                "topic": topic,
                "type": event_type
            }
            session_info["events"].append(event_info)
        
        # Add the complete session information to the specific time slot
        conference_program[session_date][session_slot].append(session_info)

    return conference_program

def get_msr_papers_range(start_year, end_year):
    all_years_papers = {}
    for year in range(start_year, end_year + 1):
        papers_by_year = get_msr_papers_by_year(year)
        if papers_by_year:
            all_years_papers[str(year)] = papers_by_year
        else:
            print(f"No data found for year {year}.")
    return all_years_papers

# Example usage
start_year = 2020  # Change to your desired start year
end_year = 2020    # Change to your desired end year
papers_data = get_msr_papers_range(start_year, end_year)
# papers_data = get_msr_papers_by_year(2018)

json_filename = 'msr_papers_data_new.json'
with open(json_filename, 'w') as json_file:
    json.dump(papers_data, json_file, indent=4)

print(f"Data has been saved to {json_filename}.")
