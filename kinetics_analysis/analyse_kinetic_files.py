import os
import pandas as pd
from sklearn.linear_model import LinearRegression

# Define directory & enzyme concentration used (in mM)
directory = '/Users/max/Downloads/eugokineticsfiles25200umsubstrate/mockdata/'
enzyme_conc = 50 /1000 /1000

def average_column(file1, file2):
    # Read in data from file1 and file2, ignore first row
    df1 = pd.read_csv(file1, skiprows=[0], index_col=0, skipinitialspace=True)
    df2 = pd.read_csv(file2, skiprows=[0], index_col=0, skipinitialspace=True)
    # Calculate average for each row of second column
    averages = (df1.iloc[:, 0] + df2.iloc[:, 0]) / 2
    # Return averages, remove empty lines from data
    return averages[averages.notna()]

# Create empty dfs to store averages and slopes
avg_df, result_df = pd.DataFrame(), pd.DataFrame()

# Iterate over files in directory
for filename in os.listdir(directory):
   if filename.endswith('1.txt'):
        # Extract number and file extension from filename
        parts = filename.split("_")
        name,conc = parts[0], float(parts[1])

        file1 = f"{directory}/{name}_{conc:g}_1.txt"
        file2 = f"{directory}/{name}_{conc:g}_2.txt"

        # Apply custom function and store in df
        avg = average_column(file1, file2)
        avg_df[conc] = avg

        # calculate linear regression, calculate & store results
        x = avg.index.values.reshape(-1, 1)
        reg = LinearRegression().fit(x, avg)
        slope = reg.coef_[0]
        result_df[conc] = (slope, slope/27, slope/27/enzyme_conc)

# Transpose the DataFrames
avg_df = avg_df.T.sort_index()
result_df = result_df.T.sort_index()

# Write the DataFrames to csv files
avg_df.to_csv(directory +'/averages.csv', index_label='t')
result_df.to_csv(directory +'/result.csv', index_label='conc', header=['A/s','mM/s','s-1'])
