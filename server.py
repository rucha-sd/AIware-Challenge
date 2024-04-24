import pandas as pd
import GA
import random

input = pd.read_csv("input.csv")
input.head()

input['id'] = range(1, len(input)+1)
for i in range(len(input)):
    # check if author is a string
    if type(input['author'][i]) != str:
        input['author'][i] = []
    else:
        input['author'][i] = input['author'][i].split(',')
input.head()

population_size = 50
max_generations = 100
crossover_probability = 0.8
mutation_probability = 0.2
num_sessions = 28


# create papers
papers = []
for i in range(len(input)):
    paper = GA.Paper(id=input['id'][i], authors=input['author'][i], duration=input['duration'][i])
    papers.append(paper)

session_lengths = [50]*num_sessions
num_tracks_per_session = [random.randint(1, 2) for _ in range(num_sessions)]

session_details = [(
    session_lengths[i],
    num_tracks_per_session[i]
) for i in range(len(session_lengths))]

# Create an instance of the GA class
ga = GA.GeneticAlgorithm(population_size, max_generations, crossover_probability, mutation_probability)

# Create the initial population
initial_population = ga.create_population(papers, session_details, population_size)
pop = GA.Population(initial_population, population_size)

pop.print_population()

# calculate fitness of the initial population and print the best solution
best = pop.best_solution(len(papers))
best[0].print_solution()

best[1]

# print fitness for all solutions
for i in range(population_size):
    print("Solution ", i, " fitness: ", pop.solutions[i].fitness(len(papers)))

# run the genetic algorithm

pop = ga.run(papers, num_sessions, session_lengths, num_tracks_per_session, population_size)
# print out results of fittest individual in final population
pop

pop[0].print_solution()
