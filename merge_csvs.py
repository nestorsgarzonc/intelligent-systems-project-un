import pandas as pd
import os

# Set the path
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
CSVS_RAW = os.listdir(BASE_PATH)
CSVS = []

# Check if the file is a csv and ends with _v2.csv
for i in range(len(CSVS_RAW)):
    if CSVS_RAW[i][-7:] == '_v2.csv':
        CSVS.append(CSVS_RAW[i])

print('#### CSVS ####')
print(CSVS)
print(len(CSVS))
print('#### END CSVS ####')

# Read the csvs into dataframes
DATAFRAMES = []
for i in CSVS:
    DATAFRAMES.append(pd.read_csv(i))

# Concatenate the dataframes
DATAFRAME = pd.concat(DATAFRAMES)

# Drop duplicates
DATAFRAME = DATAFRAME.drop_duplicates()

# PRINT THE DATAFRAME AND CHECK IF IT IS CORRECT
print('#### DATAFRAME ####')
print(DATAFRAME)
print(DATAFRAME.shape)
print('#### END DATAFRAME ####')

# Write the dataframe to a csv
DATAFRAME.to_csv('attractions.csv', index=False)
