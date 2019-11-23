import pandas as pd
import numpy as np


# =============================================================================
# path = r'D:\work\y4s1\bus intelligence\finlaproject'
# all_files = glob.glob(path + '/*.csv')
# 
# df = pd.concat((pd.read_csv(i, header=0, index_col=None) for i in all_files), ignore_index=True)
# 
# =============================================================================

# Import
df_entry = pd.read_csv('indeed_jobs_entry.csv')
df_mid = pd.read_csv('indeed_jobs_mid.csv')
df_senior = pd.read_csv('indeed_jobs_senior.csv')

# Create experience level column
df_entry['exp_lvl'] = 1
df_mid['exp_lvl'] = 2
df_senior['exp_lvl'] = 3

# Concat into 1 df
df = pd.concat([df_entry, df_mid, df_senior], ignore_index=True)
df.head()


# Cleaning
# Remove return to line mark, remove trailing spaces
for column in df:
    if column != 'direct_link' and column != 'exp_lvl':
        df[column] = df[column].str.replace('\n', ' ')
        df[column].str.strip()

df.head()

# Remove duplicate postings
df.drop_duplicates(subset=['job_title', 'company_name'], keep='first', inplace=True)

### Processing salary column
# Strip unnecessary character
# Take average for ranges of salary
# Convert hourly to yearly rate
df['yearly_avg_salary'] = df.salary.str.replace(r'[a-zA-Z]', '').str.replace('$','').str.replace(',','').str.replace(' ','').replace('','0-0')
df.yearly_avg_salary = df.yearly_avg_salary.str.split('-', expand=True).astype(float).mean(axis=1)
df.yearly_avg_salary.replace(0, np.NaN, inplace=True)
df.loc[df.yearly_avg_salary<500, 'yearly_avg_salary'] *= 1900

# Export to csv
df.to_csv('full_dataset_clean.csv', index=False)



      







              
                    
                    
