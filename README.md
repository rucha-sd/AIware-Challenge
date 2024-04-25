## Project Overview

This project is designed to automate the processing and scheduling of academic papers in a conference considering logistical constraints and topic coherence within sessions. The pipeline includes scripts for extracting data from web sources, converting JSON data into a more manageable CSV format, preprocessing the data, and finally optimizing the paper scheduling using a genetic algorithm.

### Scripts and Their Functions

1. **extract.py**:
   - **Purpose**: Scrapes JSON objects from MSR data links for specified years.
   - **Usage**: `python3 extract.py`
   - **Parameters**: 
     - `start_year`: The beginning year for data extraction.
     - `end_year`: The ending year for data extraction.

2. **parseSessionsCSV**:
   - **Purpose**: Converts JSON data into a CSV file, placing each paper in a separate row.
   - **Usage**: `python3 parseSessionsCSV <filename.json> <filename.csv>`

3. **preprocess_data**:
   - **Purpose**: Prepares data for the main algorithm by preprocessing the extracted and parsed data.
   - **Usage**: Refer to internal documentation or script help.

4. **GA.py**:
   - **Purpose**: Contains all logic for the genetic algorithm, managing objects such as Papers, Solution, Session, Population, and Genetic Algorithm itself.
   - **Usage**: Integrated within the pipeline, not run independently.

5. **pipeline.py**:
   - **Purpose**: Orchestrates the entire process from data preprocessing to genetic algorithm execution.
   - **Usage**: `python3 pipeline.py <population_size> <num_of_generations> <input.csv> > <output_file.txt>`
   - **Example**: `python3 pipeline.py 100 1000 input.csv > output_file.txt`
   - **Parameters**:
     - `population_size`: Number of schedules per generation.
     - `num_of_generations`: Total number of generations to create.
     - `input.csv`: The preprocessed CSV file containing the papers to schedule.

### Running the Pipeline

To run the complete pipeline and generate the optimal schedule for the papers, use the following command:

```bash
python3 pipeline.py 100 1000 input.csv > output_file.txt
```

This command processes the `input.csv` to create 1000 generations of paper schedules, with each generation consisting of 100 different schedules. The best schedule is then output to `output_file.txt`.

### Additional Information

Refer to the comments within each script for more detailed instructions on parameters and configurations. Ensure that all dependencies are installed and that Python 3.x is being used.

