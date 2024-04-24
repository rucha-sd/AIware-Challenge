import sys
import preprocess_data
import GA
import pandas as pd


# main function
if __name__ == '__main__':
    args = sys.argv
    input_file = args[1]
    population_size = 50
    max_generations = 100
    crossover_probability = 0.8
    mutation_probability = 0.2

    parsed_input_file, papers_dicts = preprocess_data.parse_csv_to_array(input_file)
    session_durations, num_tracks_per_session = preprocess_data.session_details(parsed_input_file)
    session_details = [(session_durations, num_tracks_per_session)]

    ga = GA.GeneticAlgorithm(population_size, max_generations, crossover_probability, mutation_probability)
    papers = preprocess_data.create_papers(input_file)
    papers_array = [x for x in papers.values()]
    
    solutions_from_csv = preprocess_data.merge_overlaps(papers_dicts)

    for item in solutions_from_csv:
        for key, paper_ids in solutions_from_csv[item].items():
            val = [papers[int(ids)] for ids in paper_ids]
            solutions_from_csv[item][key] = val
            
         
    for time_slot, rooms in solutions_from_csv.items():
        print("###############")
        print(f"Time Slot: {time_slot}")
        for room, papers in rooms.items():
            print(room)
            print([paper.print_paper() for paper in papers])
            print("\n")