import pandas as pd

df = pd.read_csv('indeed_jobs.csv')

# Cleaning
# Remove return to line mark, remove trailing spaces
for column in df:
    if column != 'direct_link':
        df[column] = df[column].str.replace('\n', ' ')
    df[column].str.strip()

df.head()
