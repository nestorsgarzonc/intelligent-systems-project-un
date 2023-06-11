import os
import pandas as pd

# Set the path to the raw data
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
CSVS_RAW = os.listdir(BASE_PATH)
CSVS = []
# Remove data that is not a csv
for i in range(len(CSVS_RAW)):
    if CSVS_RAW[i][-4:] == '.csv':
        CSVS.append(CSVS_RAW[i])


def get_path_for_file(file: str) -> str:
    return os.path.join(BASE_PATH, file)


# Read the csvs into dataframes
for i in CSVS:
    print('Cleaning ' + i)
    csv = pd.read_csv(get_path_for_file(i))
    rows_to_drop = []
    for j in range(len(csv)):
        print('Cleaning row ' + str(j))
        # Remove rows that are reviews
        if csv['url'][j].endswith('#REVIEWS'):
            print('Removing row ' + str(j))
            rows_to_drop.append(j)
        # Remove rows that name is not a string or is null
        if type(csv['name'][j]) != str or csv['name'][j] == 'null' or csv['name'][j] == None or csv['name'][j] == '':
            print('Removing row ' + str(j))
            rows_to_drop.append(j)
    # Write the cleaned dataframes to csvs
    csv = csv.drop(list(set(rows_to_drop)))
    print('Saving' + i)
    csv.to_csv(i, index=False)
