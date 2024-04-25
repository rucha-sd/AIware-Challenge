#Extract.py :

This file is used to get webscraped json objects from the web links of msr data. 

Command - python3 extract.py

arguments to change : start_year and end_year - eg: 2018 till 2019


#parseSessionsCSV:

This file is used to convert the json to csv which will give us the individual papers as rows.

command - python3 parseSessionsCSV

Arguments - filename.json to filename.csv

#preprocess_data

We use this file to prepare data for the main job.

#GA.py 

GA file manages all the algorithmic logic along with the various objects that will be used while computing the solutions.
It contains the objects:
  Papers
  Solution
  Session
  Population
  Genetic Algorithm

The main file that holds everything together is the pipeline file.

To run the pipelien file use the command:

python3 pipeline.py population_size num_of_generations Year > output_file.txt

eg: python3 pipeline.py 100 1000 input.csv > output_file.txt 

The above command will run the algorithm to compute the best schedule for the papers in the input.csv file. The algorithm creates 1000 generations and each generation with 100 population , i.e 100 schedules per generation. 
