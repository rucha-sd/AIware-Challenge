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

    parsed_input_file, papers_dicts = preprocess_data.parse_csv_to_array(input_file)
    session_durations, num_tracks_per_session = preprocess_data.session_details(parsed_input_file)
    session_details = [(session_durations[i], num_tracks_per_session[i]) for i in range(len(session_durations))]
    ga = GA.GeneticAlgorithm(population_size, max_generations, crossover_probability, mutation_probability)
    papers = preprocess_data.create_papers(input_file)
    papers_array = [x for x in papers.values()]
    
    initial_population = ga.create_population(papers_array, session_details, population_size)
    pop = ga.run(papers_array, len(num_tracks_per_session), session_durations, num_tracks_per_session, population_size, args[4])
    pop[0].print_solution()
    print(pop[1])

    # solutions_from_csv = preprocess_data.merge_overlaps(papers_dicts)
    # solutions = preprocess_data.create_solution(solutions_from_csv, papers)

    # #printing our solutions         
    # for time_slot, rooms in solutions.items():
    #     print("###############")
    #     print(f"Time Slot: {time_slot}")
    #     for room, papers in rooms.items():
    #         print(room)
    #         for paper in papers:
    #             print(paper.print_paper())
    #         print("\n")