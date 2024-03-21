class Paper:
    def __init__(self, id, authors, duration, topic=None):
        self.id = id
        self.authors = authors
        self.duration = duration
        self.topic = topic

class Session:
    def __init__(self, max_length, tracks):
        self.tracks = tracks  # A list of lists, each sublist is a track of papers
        self.max_length = max_length  # Maximum duration of the session


class Solution:
    def __init__(self, sessions):
        self.sessions = sessions  # A list of Session objects


class Population:
    def __init__(self, solutions):
        self.solutions = solutions  # A list of Solution objects

    def print_population(self):
        for i, solution in enumerate(self.solutions):
            print(f"Solution {i+1}:")
            for j, session in enumerate(solution.sessions):
                print(f"  Session {j+1} (Max length: {session.max_length} minutes):")
                for k, track in enumerate(session.tracks):
                    track_duration = sum(paper.duration for paper in track)
                    print(f"    Track {k+1} (Total duration: {track_duration} minutes):")
                    for paper in track:
                        print(f"      Paper ID: {paper.id}, Authors: {', '.join(paper.authors)}, Duration: {paper.duration} minutes")
            print("-" * 40) 