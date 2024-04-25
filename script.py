import os

# Parameters
pop = 100
gen_values = range(1000, 11000, 1000)  # From 1000 to 10000, incrementing by 1000
year_values = range(2022, 2023)  # From 2018 to 2023

# Iterate over each year and gen value
for year in year_values:
    for gen in gen_values:
        # Construct the input CSV file path
        csv_file = f'csv/conference_schedule_{year}.csv'
        
        # Construct the output directory and file path
        output_dir = f'output/{year}'
        output_file = f'{output_dir}/{pop}_{gen}_{year}.txt'
        
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Construct the command
        command = f'python3 pipeline.py {csv_file} {pop} {gen} {year} > {output_file}'
        
        # Execute the command
        os.system(command)

print("Finished running all pipeline commands.")
