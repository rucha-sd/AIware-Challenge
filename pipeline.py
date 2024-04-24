import sys
import preprocess_data
import GA
import pandas as pd


# main function
if __name__ == '__main__':
    args = sys.argv
    input_file = args[1]
    population_size = int(args[2])
    max_generations = int(args[3])
    crossover_probability = 0.8
    mutation_probability = 0.2

    print(f'population_size: {population_size} max_generations: {max_generations}')

    parsed_input_file = preprocess_data.parse_csv_to_array(input_file)
    session_durations, num_tracks_per_session = preprocess_data.session_details(parsed_input_file)
    print(session_durations[0])
    session_details = [(session_durations[i], num_tracks_per_session[i]) for i in range(len(session_durations))]
    # print(num_tracks_per_session)
    ga = GA.GeneticAlgorithm(population_size, max_generations, crossover_probability, mutation_probability)
    input = pd.read_csv("input.csv")
    papers = preprocess_data.create_papers(input_file)
    initial_population = ga.create_population(papers, session_details, population_size)
    pop = GA.Population(initial_population, population_size)
    pop = ga.run(papers, len(num_tracks_per_session), session_durations, num_tracks_per_session, population_size, args[4])
    pop[0].print_solution()
    print(pop[1])
    