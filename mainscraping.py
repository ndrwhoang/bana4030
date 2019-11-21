import pandas as pd
from bs4 import BeautifulSoup
import requests

def indeed_job_scrape(keyword, search_location, no_page, job_type='None', exp_lvl='None'):
    ### 'keyword' transformation to fit in with url
    keyword = keyword.replace(' ','+')
    ### exp_level number convert to query arguement
    if exp_lvl == 1:
        exp_lvl_str = 'entry_level'
    elif exp_lvl == 2:
        exp_lvl_str = 'mid_level'
    elif exp_lvl == 3:
        exp_lvl_str = 'senior_level'
    else:
        raise ValueError('exp_lvl only accpets 1, 2, or 3')
    
    ### Data to scrape
    # Job title
    j_title = []
    # Company name
    company_name = []
    # Salary
    salary = []
    # Location
    location = []
    # Rating
    company_rating = []
    # Posting link
    hyperlink = []
    # Posting description
    j_desc = []
    
    ### Main scraping loop
    for page_index in range(0, no_page*10, 10):
        page = 'https://www.indeed.com/jobs?q=' + keyword + '&l=' + search_location + '&jt=' + job_type + '&explvl=' + exp_lvl_str + '&start=' + str(page_index)
        print(page)
        page_response = requests.get(page, timeout=5)
        main_soup = BeautifulSoup(page_response.text, 'html5lib')
        for i in main_soup.find_all('div', {'class':'jobsearch-SerpJobCard'}):
            # Position title
            j_title.append(i.find('a', {'class':'jobtitle'})['title']) 
            # Company name                       
            company_name.append(i.find('span', {'class':'company'}).text)
            # Salary (if information available, 'None' otherwise)                        
            salary.append(i.find('span', {'class':'salaryText'}).text if i.find('span', {'class':'salaryText'}) else 'None')  
            # Job location                             
            location.append(i.find(attrs={'class':'location'}).text)
            # Comapny rating
            company_rating.append(i.find('span', {'class':'ratingsContent'}).text if i.find('span', {'class':'ratingsContent'}) else 'None')
            # Link to detailed job posting
            hyperlink.append('https://www.indeed.com/' + str(i.find('a', {'class':'jobtitle'})['href']))
            # Fulljob description
            url = 'https://www.indeed.com/' + str(i.find('a', {'class':'jobtitle'})['href'])
            url_response = requests.get(url, timeout=5)
            soupy_soup = BeautifulSoup(url_response.text, 'html5lib')
            j_desc.append(soupy_soup.find('div', {'id':'jobDescriptionText'}).text)
    
    ### Save to pandas dataframe 
    df_local = pd.DataFrame({'job_title' : j_title,
                       'company_name' : company_name,
                       'salary' : salary,
                       'job_location' : location,
                       'direct_link' : hyperlink,
                       'full_description' : j_desc})
    return df_local

# Scraping , first arguement is keyword, second location, thrid number of pages (~19 postings per pages)
# job type and experience level optional
# 1 for entry level jobs, 2 for mid level, and 3 for senior level
df = indeed_job_scrape('information technology', 'Ohio', no_page=20, exp_lvl=2)

pd.options.display.max_columns = 50
df.head()

# Make a copy for each exp level, change the variable accordingly
df_mid = df.copy()

# Export csv to current working directory
df_entry.to_csv('indeed_jobs_entry.csv', index=False)
df_mid.to_csv('indeed_jobs_mid.csv', index=False)
df_senior.to_csv('indeed_jobs_senior.csv', index=False)
