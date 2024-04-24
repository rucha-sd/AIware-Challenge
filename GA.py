import random
import matplotlib.pyplot as plt
from tqdm import tqdm
import copy
import math

class Paper:
    def __init__(self, id, authors, duration, topic=None):
        self.id = id
        self.authors = authors
        self.duration = duration
        topics = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.topic = random.choice(topics) if topic is None else topic
    def print_paper(self):
        return f"ID: {self.id}, Authors: {self.authors}, Duration: {self.duration}, Topic: {self.topic}"    

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
        total_time_unused = 0
        papers_scheduled = set() 
        total_authors = set()

        for session in self.sessions:
            actual_duration = 0
            session_time_unused = 0
            # create a list of sets that contains authors in each track
            authors_in_session = [set() for _ in range(len(session.tracks))]
            for i in range(len(session.tracks)):
                track = session.tracks[i]
                track_duration = sum(paper.duration for paper in track)

                session_time_unused += max(0, session.max_length - track_duration)
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
                    total_authors.update(paper.authors)
                                
            # make a list that contains all the authors in the session, keep duplicates
            # print(len(session.tracks))
            all_authors = []
            for authors_set in authors_in_session:
                all_authors.extend(authors_set)
            # Penalize for repeating authors
            author_penalty += len(all_authors) - len(set(all_authors))
            total_time_unused += session_time_unused

        # Penalize if a paper is not scheduled at all
        distribution_penalty = num_papers - len(set(papers_scheduled))

        cohrence_penalty = 0

        # for all tracks calculate topic similarity of paper using entropy to get thematic coherence
        for session in self.sessions:
            for track in session.tracks:
                if len(track)<=1:
                    continue
                # create a list of topics of the papers in the track
                topics = [paper.topic for paper in track]
                # calculate entropy of the topics
                entropy = 0
                for topic in set(topics):
                    p = topics.count(topic) / len(topics)
                    entropy -= p * math.log2(p)
                # cohrence_penalty += 2*entropy / len(set(topics))
                cohrence_penalty += entropy / math.log2(len(track))
        

        total_tracks = sum(len(session.tracks) for session in self.sessions)
        # print all penalties for the solution
        # print(f"Time Penalty: {time_penalty}, Author Penalty: {author_penalty}, Distribution Penalty: {distribution_penalty}, Duration Penalty: {total_time_unused}")
        # scale the penalties
        # total_time_unused = total_time_unused / total_time available*100
        # time_penalty = time_penalty / total_time available*100
        # author_penalty = author_penalty / total authors*100
        # distribution_penalty = distribution_penalty / total papers*100
 
        # print("Max length")
        # print([session.max_length for session in self.sessions])
        # calcukate scaled penalties
        total_time_available = sum([session.max_length for session in self.sessions])
        weighted_time_penalty = (time_penalty / total_time_available) * 100
        weighted_author_penalty = (author_penalty / len(total_authors)) * 100
        weighted_distribution_penalty = (distribution_penalty / num_papers) * 100
        weighted_total_time_unused = (total_time_unused / total_time_available) * 100
        # weighted_coherence_penalty = (cohrence_penalty / total_tracks) * 100
        weighted_coherence_penalty = cohrence_penalty 
        # print(weighted_coherence_penalty)
    
        # total_penalty
        total_penalty = 10*weighted_time_penalty + 10*weighted_author_penalty + 10*weighted_distribution_penalty + weighted_total_time_unused + weighted_coherence_penalty

        fitness = 1 / (1 + total_penalty)

        # return inididual penalties and fitness
        return {
            'total_time_available': total_time_available,
            'total_time_unused': total_time_unused,
            'weighted_time_penalty': weighted_time_penalty,
            'weighted_author_penalty': weighted_author_penalty,
            'weighted_distribution_penalty': weighted_distribution_penalty,
            'weighted_total_time_unused': weighted_total_time_unused,
            'weighted_coherence_penalty': weighted_coherence_penalty,
            'total_penalty': total_penalty,
            'fitness': fitness
        }


    
    def print_solution(self):
        for i, session in enumerate(self.sessions):
            print(f"Session {i+1} (Max length: {session.max_length} minutes):")
            for j, track in enumerate(session.tracks):
                track_duration = sum(paper.duration for paper in track)
                print(f"  Track {j+1} (Total duration: {track_duration} minutes):")
                for paper in track:
                    print(f"    Paper ID: {paper.id}, Authors: {', '.join(paper.authors)}, Topic: {paper.topic},  Duration: {paper.duration} minutes")
            print("-" * 40)
                                            
class Population:
    def __init__(self, solutions, population_size):
        self.solutions = solutions  
        self.population_size = population_size

    def print_population(self):
        for i, solution in enumerate(self.solutions):
            print(f"Solution {i+1}:")
            solution.print_solution()

    def best_solution(self, num_papers):
        best_solution = self.solutions[0]
        for solution in self.solutions:
            if solution.fitness(num_papers)['fitness'] > best_solution.fitness(num_papers)['fitness']:
                best_solution = solution
        return best_solution, best_solution.fitness(num_papers)

class GeneticAlgorithm:
    def __init__(self, population_size, max_generations, crossover_probability, mutation_probability):
        self.population_size = population_size
        self.max_generations = max_generations
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        random.seed(42)
        

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

        # swap_probability = 0.5
        # move_probability = 0.5

        # print(solution.print_solution())

        solution_copy = copy.deepcopy(solution)
        # check if session is empty i.e none of the tracks have any papers. select session_to_mutate as non empty session
        session_to_mutate = random.choice(solution_copy.sessions)


        while not any([len(track) for track in session_to_mutate.tracks]):
        # while not any(session_to_mutate.tracks):
            # print("Finding mutation session")
            session_to_mutate = random.choice(solution_copy.sessions)


        # if random.random() < swap_probability:
        # print("Swap Mutation")
        if len(session_to_mutate.tracks) > 1:
            # swap two papers between two tracks
            track1, track2 = random.sample(session_to_mutate.tracks, 2)
            while track1 == track2:
                print("Track1: ", track1, "Track2: ", track2)
                track1, track2 = random.sample(session_to_mutate.tracks, 2)
            
            if track1 and track2:
                paper1 = random.choice(track1)
                paper2 = random.choice(track2)
                track1.append(paper2)
                track2.append(paper1)
                track1.remove(paper1)
                track2.remove(paper2)                
                 

        # if random.random() < move_probability:
        # move paper from one session to another
        # print("Move Mutation")
        session_from, session_to = 0, 0
        while session_from == session_to:
            session_from, session_to = random.sample(solution_copy.sessions, 2)
            # print(session_from, session_to)

        track_from = random.choice(session_from.tracks)
        track_to = random.choice(session_to.tracks)
        if track_from and track_to:
            paper = random.choice(track_from)
            track_to.append(paper)
            track_from.remove(paper)

        return solution_copy

            # session_from = random.choice(solution.sessions)
            # session_to = random.choice(solution.sessions)
            # track_from = random.choice(session_from.tracks)
            # track_to = random.choice(session_to.tracks)
            # paper_to_move = random.choice(track_from)
            # track_to.append(paper_to_move)
            # track_from.remove(paper_to_move)

    def select_parents(self, population, num_papers, tournament_size=3):
        def tournament():
            # print("Population size in tournament: ", len(population.solutions))
            contenders = random.sample(population.solutions, tournament_size)
            # print("Contenders: ", contenders)
            best = sorted(contenders, key=lambda solution: solution.fitness(num_papers)['fitness'], reverse=True)[0]
            return best

        parent1 = tournament()
        parent2 = tournament()
        while parent1 == parent2:  # Ensure parent1 and parent2 are not the same
            # print("Parent1 and Parent2 are the same")
            # print(parent1, parent2)
            parent2 = tournament()
        return parent1, parent2

    def select_survivors(self, population, new_population, num_papers):
        combined_population = population.solutions + new_population.solutions
        sorted_combined_population = sorted(combined_population, key=lambda solution: solution.fitness(num_papers)['fitness'], reverse=True)
        survivors = sorted_combined_population[:self.population_size]
        return Population(survivors, self.population_size)
    
    def plot_progress(self, fitness_values, time_penalties, author_penalties, distribution_penalties, coherence_penalties, year):
        fig, axs = plt.subplots(2, 2)
        # increase figure size
        fig.set_size_inches(12, 8)
        fig.suptitle('Penalties and Fitness Value over Generations')
        axs[0, 0].plot(time_penalties)
        axs[0, 0].set_title('Weighted Time Penalty')
        axs[0, 1].plot(author_penalties)
        axs[0, 1].set_title('Weighted Author Penalty')
        axs[1, 0].plot(distribution_penalties)
        axs[1, 0].set_title('Weighted Distribution Penalty')
        axs[1, 1].plot(coherence_penalties)
        axs[1, 1].set_title('Weighted Coherence Penalty')
        plt.savefig(f'fitness_values_{self.population_size}_{self.max_generations}_{year}_2.png')
        plt.show()
        # new plot
        plt.clf()
        # plot graph of fitness values over generations
        plt.plot(fitness_values)
        plt.xlabel('Generation')    
        plt.ylabel('Fitness Value')
        plt.title('Fitness Value over Generations')
        # save with pop_size, num_generations
        plt.savefig(f'fitness_values_{self.population_size}_{self.max_generations}_{year}_1.png')
        plt.show()
        

    def run(self, papers, num_sessions, session_lengths, num_tracks, num_solutions, year):
        session_details = [(session_lengths[i], num_tracks[i]) for i in range(len(session_lengths))]
        fitness_values = []
        time_penalties = []
        author_penalties = []
        distribution_penalties = []
        coherence_penalties = []
        population = Population(self.create_population(papers, session_details, num_solutions), num_solutions)
        for generation in tqdm(range(self.max_generations)):
            # print("Generation %d" % generation)
            new_population = []
            # implement elitism, keep 10% best population
            population.solutions = sorted(population.solutions, key=lambda solution: solution.fitness(len(papers))['fitness'], reverse=True)
            new_population.extend(population.solutions[:int(0.1 * self.population_size)])
            while len(new_population) < self.population_size:
                parent1, parent2 = self.select_parents(population, len(papers))
                if random.random() < self.crossover_probability:
                    child = self.crossover(parent1, parent2)
                else:
                    child = parent1
                if random.random() < self.mutation_probability:
                    child = self.mutate(child)
                new_population.append(child)
            population = self.select_survivors(population, Population(new_population, self.population_size), len(papers))
            # get best fitness
            best_solution, fitness = population.best_solution(len(papers))
            fitness_values.append(fitness['fitness'])
            time_penalties.append(fitness['weighted_time_penalty'])
            author_penalties.append(fitness['weighted_author_penalty'])
            distribution_penalties.append(fitness['weighted_distribution_penalty'])
            coherence_penalties.append(fitness['weighted_coherence_penalty'])
            
        # plot fitness values over generations
        self.plot_progress(fitness_values, time_penalties, author_penalties, distribution_penalties, coherence_penalties, year)
        return population.best_solution(len(papers))
    