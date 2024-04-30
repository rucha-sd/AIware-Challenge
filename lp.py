import pulp
import preprocess_data
import importlib

def have_common_authors(paper1, paper2):
    return not set(paper1.authors).isdisjoint(paper2.authors)
# Reload the data processing module
importlib.reload(preprocess_data)
input_file = "./csv/conference_schedule_2021.csv"

# Parse the CSV file and create a list of session details and papers
parsed_input_file, papers_schedule = preprocess_data.parse_csv_to_array(input_file)
session_durations, num_tracks_per_session = preprocess_data.session_details(parsed_input_file)
session_details = list(zip(session_durations, num_tracks_per_session))
papers = preprocess_data.create_papers(input_file).values()

# Initialize the problem
prob = pulp.LpProblem("Conference_Schedule", pulp.LpMinimize)

# Set up the decision variables
x = pulp.LpVariable.dicts("paper_schedule", 
                          [(i.id, j, k) for i in papers
                                     for j in range(len(session_details))
                                     for k in range(max(num_tracks_per_session))],
                          cat='Binary')

# The objective function could be refined to a more suitable one
# For example, to minimize the last session number where a paper is scheduled (to make the schedule as compact as possible)
prob += pulp.lpSum(j * x[paper.id, j, k] for paper in papers for j in range(len(session_details)) for k in range(max(num_tracks_per_session)))

# Constraint 1: Each paper is scheduled exactly once
for paper in papers:
    prob += pulp.lpSum(x[paper.id, j, k] for j in range(len(session_details)) for k in range(max(num_tracks_per_session))) == 1

# Constraint 2: Total duration of papers in a session cannot exceed session duration
for j, (session_duration, num_of_tracks) in enumerate(session_details):
    for k in range(num_of_tracks):
        prob += pulp.lpSum(x[paper.id, j, k] * paper.duration for paper in papers) <= session_duration

# Constraint 3: Papers with common authors cannot be scheduled in parallel
for paper1 in papers:
    for paper2 in papers:
        if paper1 != paper2 and have_common_authors(paper1, paper2):
            for j in range(len(session_details)):
                for k in range(num_tracks_per_session[j]):
                    for l in range(k+1, num_tracks_per_session[j]):
                        prob += x[paper1.id, j, k] + x[paper2.id, j, l] <= 1

# Constraint 4: Papers with the same topic should be scheduled in the same session, but can be on different tracks
for topic in set(paper.topic for paper in papers):
    for j in range(len(session_details)):
        topic_papers = [paper.id for paper in papers if paper.topic == topic]
        for m in range(num_tracks_per_session[j]):
            prob += pulp.lpSum(x[paper_id, j, m] for paper_id in topic_papers) <= num_tracks_per_session[j]
            for paper_id in topic_papers:
                prob += x[paper_id, j, m] >= x[paper_id, j, 0]

# Solve the problem
status = prob.solve()

# Output results or debug information
if status == pulp.LpStatusOptimal:
    print("Optimal solution found!")
    for v in prob.variables():
        if v.varValue == 1:
            print(v.name, "=", v.varValue)
elif status == pulp.LpStatusInfeasible:
    print("Problem is still infeasible after relaxation.")
else:
    print("Problem could not be solved. Status:", pulp.LpStatus[status])
