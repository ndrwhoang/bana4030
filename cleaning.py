import pandas as pd

df = pd.read_csv('indeed_jobs.csv')

# Cleaning
# Remove trailing spaces and return to line
for column in df:
    if column != 'direct_link' and column != 'salary':
        df[column] = df[column].str.replace('\n', ' ')
