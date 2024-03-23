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

    def fitness(self, num_papers):
        time_penalty = 0
        author_penalty = 0
        distribution_penalty = 0

        # total_possible_duration = sum(session.max_length for session in self.sessions)
        total_time_unused = 0
        papers_scheduled = set() 

        for session in self.sessions:
            actual_duration = 0
            total_time_unused = 0
            # create a list of sets that contains authors in each track
            authors_in_session = [set() for _ in range(len(session.tracks))]
            for i in range(len(session.tracks)):
                track = session.tracks[i]
                track_duration = sum(paper.duration for paper in track)

                total_time_unused += session.max_length - track_duration
                # for paper in track:    
                    # Penalize if a track exceeds the session's max_length
                if track_duration > session.max_length:
                    time_penalty += (track_duration - session.max_length)

                for paper in track:
                    papers_scheduled.add(paper.id)
                    # Check for author overlap within the same session's parallel tracks
                    for author in paper.authors:
                        # check if the author is present in any of the previous tracks
                        authors_in_session[i].add(author)
                                
            # make a list that contains all the authors in the session, keep duplicates
            all_authors = [author in authors_in_session[i] for i in range(len(session.tracks))]
            # Penalize for repeating authors
            author_penalty += len(all_authors) - len(set(all_authors))

        # Penalize if a paper is not scheduled at all
        distribution_penalty += num_papers - len(papers_scheduled)
        # print all penalties for the solution
        print(f"Time Penalty: {time_penalty}, Author Penalty: {author_penalty}, Distribution Penalty: {distribution_penalty}, Duration Penalty: {total_time_unused}")

        total_penalty = total_time_unused + time_penalty + author_penalty + distribution_penalty

        return 1 / (1 + total_penalty)


    
    def print_solution(self):
        for i, session in enumerate(self.sessions):
            print(f"Session {i+1} (Max length: {session.max_length} minutes):")
            for j, track in enumerate(session.tracks):
                track_duration = sum(paper.duration for paper in track)
                print(f"  Track {j+1} (Total duration: {track_duration} minutes):")
                for paper in track:
                    print(f"    Paper ID: {paper.id}, Authors: {', '.join(paper.authors)}, Duration: {paper.duration} minutes")
            print("-" * 40)
                    
                        
class Population:
    def __init__(self, solutions):
        self.solutions = solutions  

    def print_population(self):
        for i, solution in enumerate(self.solutions):
            print(f"Solution {i+1}:")
            solution.print_solution()

    def best_solution(self, num_papers):
        best_solution = self.solutions[0]
        for solution in self.solutions:
            if solution.fitness(num_papers) > best_solution.fitness(num_papers):
                best_solution = solution
        return best_solution, best_solution.fitness(num_papers)


class GeneticAlgorithm:
    def __init__(self, population_size, max_generations, crossover_probability, mutation_probability):
        self.population_size = population_size
        self.max_generations = max_generations
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability

    def create_population(self, papers,  session_details, population_size):
        population = []

        for _ in range(population_size):
            sessions = []
            papers_copy = papers[:] 
            random.shuffle(papers_copy)

            for details in session_details:
                max_length, num_tracks = details
                session = Session(max_length=max_length, tracks=[[] for _ in range(num_tracks)])
                current_track = 0
                for paper in papers_copy:
                    if sum(p.duration for p in session.tracks[current_track]) + paper.duration <= session.max_length:
                        session.tracks[current_track].append(paper)
                        papers_copy.remove(paper)
                    current_track = (current_track + 1) % num_tracks
                    if current_track == 0 and not papers_copy:  
                        break
                sessions.append(session)
            solution = Solution(sessions)
            population.append(solution)
        return population


    def evaluate_population(self, population):
        pass

    def crossover(self, parent1, parent2):
        crossover_point = random.randint(1, len(parent1.sessions) - 2)
        child_sessions = parent1.sessions[:crossover_point]
        added_papers = {paper.id for session in child_sessions for track in session.tracks for paper in track}
        for session in parent2.sessions[crossover_point:]:
            new_session_tracks = []
            for track in session.tracks:
                new_track = []
                for paper in track:
                    if paper.id not in added_papers:
                        new_track.append(paper)
                        added_papers.add(paper.id)
                new_session_tracks.append(new_track)
            child_sessions.append(Session(session.max_length, new_session_tracks))
        return Solution(child_sessions)

    def mutate(self, solution):
        # session_to_mutate = random.choice(solution.sessions)
        # track_index1, track_index2 = random.sample(range(len(session_to_mutate.tracks)), 2)
        # if random.random() < 0.5:  # Swap two papers between tracks
        #     if session_to_mutate.tracks[track_index1] and session_to_mutate.tracks[track_index2]:
        #         paper_index1 = random.randint(0, len(session_to_mutate.tracks[track_index1]) - 1)
        #         paper_index2 = random.randint(0, len(session_to_mutate.tracks[track_index2]) - 1)
        #         session_to_mutate.tracks[track_index1][paper_index1], session_to_mutate.tracks[track_index2][paper_index2] = \
        #         session_to_mutate.tracks[track_index2][paper_index2], session_to_mutate.tracks[track_index1][paper_index1]
        # else:  
        #     random.shuffle(session_to_mutate.tracks[track_index1])

        swap_probability = 0.5
        move_probability = 0.5

        session_to_mutate = random.choice(solution.sessions)

        if random.random() < swap_probability:
            if len(session_to_mutate.tracks) > 1:
                track1, track2 = random.sample(session_to_mutate.tracks, 2)
                if track1 and track2:
                    paper1 = random.choice(track1)
                    paper2 = random.choice(track2)
                    track1.append(paper2)
                    track2.append(paper1)
                    track1.remove(paper1)
                    track2.remove(paper2)   

        if random.random() < move_probability:
            # move paper from one session to another
            session_from = random.choice(solution.sessions)
            session_to = random.choice(solution.sessions)
            track_from = random.choice(session_from.tracks)
            track_to = random.choice(session_to.tracks)
            paper_to_move = random.choice(track_from)
            track_to.append(paper_to_move)
            track_from.remove(paper_to_move)
        

    def select_parents(self, population, num_papers, tournament_size=3):
        def tournament():
            contenders = random.sample(population.solutions, tournament_size)
            best = sorted(contenders, key=lambda solution: solution.fitness(num_papers), reverse=True)[0]
            return best

        parent1 = tournament()
        parent2 = tournament()
        while parent1 == parent2:  # Ensure parent1 and parent2 are not the same
            parent2 = tournament()
        return parent1, parent2

    def select_survivors(self, population, new_population, num_papers):
        combined_population = population.solutions + new_population.solutions
        sorted_combined_population = sorted(combined_population, key=lambda solution: solution.fitness(num_papers), reverse=True)
        survivors = sorted_combined_population[:self.population_size]
        return Population(survivors)

    def run(self, papers, num_sessions, session_lengths, num_tracks, num_solutions):
        session_details = [(session_lengths[i], num_tracks[i]) for i in range(len(session_lengths))]

        population = Population(self.create_population(papers, session_details, num_solutions))
        for generation in range(self.max_generations):
            new_population = []
            for _ in range(self.population_size):
                parent1, parent2 = self.select_parents(population, len(papers))
                if random.random() < self.crossover_probability:
                    child = self.crossover(parent1, parent2)
                else:
                    child = parent1
                if random.random() < self.mutation_probability:
                    self.mutate(child)
                new_population.append(child)
            population = self.select_survivors(population, Population(new_population), len(papers))
        return population.best_solution(len(papers))
    