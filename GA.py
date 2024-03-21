import random

class Paper:
    def __init__(self, id, authors, duration, topic=None):
        self.id = id
        self.authors = authors
        self.duration = duration
        self.topic = topic

class Session:
    def __init__(self, max_length, tracks):
        self.tracks = tracks  
        self.max_length = max_length  


class Solution:
    def __init__(self, sessions):
        self.sessions = sessions  

class Population:
    def __init__(self, solutions):
        self.solutions = solutions  

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


class GeneticAlgorithm:
    def __init__(self, population_size, max_generations, crossover_probability, mutation_probability):
        self.population_size = population_size
        self.max_generations = max_generations
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability

    def create_population(self, papers, num_tracks_per_session, session_lengths, population_size):
        population = []

        for _ in range(population_size):
            sessions = []
            papers_copy = papers[:] 
            random.shuffle(papers_copy)

            for session_length in session_lengths:
                session = Session(max_length=session_length, tracks=[[] for _ in range(num_tracks_per_session)])
                current_track = 0
                for paper in papers_copy:
                    if sum(p.duration for p in session.tracks[current_track]) + paper.duration <= session_length:
                        session.tracks[current_track].append(paper)
                        papers_copy.remove(paper)
                    current_track = (current_track + 1) % num_tracks_per_session
                    if current_track == 0 and not papers_copy:  
                        break
                sessions.append(session)
            solution = Solution(sessions)
            population.append(solution)
        return population


    def evaluate_population(self, population):
        pass

    def crossover(self, parent1, parent2):
        pass

    def mutate(self, solution):
        pass

    def select_parents(self, population):
        pass

    def select_survivors(self, population, new_population):
        pass

    def run(self, num_sessions, max_length, tracks, num_solutions):
        pass