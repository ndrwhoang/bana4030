import pandas as pd
import numpy as np

# Plotly
import plotly.offline as py
import plotly.graph_objs as go
import plotly.tools as tls

# Misc
from collections import Counter
import scipy
from matplotlib.pyplot import imread
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from matplotlib import pyplot as plt
%matplotlib inline
pd.options.display.max_columns = 10
np.random.seed(42)

df = pd.to_csv('full_dataset_clean.csv')

# Frequency of job level
plt.bar(10, len(df.exp_lvl[df.exp_lvl==1]), label='Entry Level')
plt.bar(15, len(df.exp_lvl[df.exp_lvl==2]), label='Mid Level')
plt.bar(20, len(df.exp_lvl[df.exp_lvl==3]), label='Senior Level')
plt.legend(loc=4)

### Exploring salary information
# df[df>0].groupby('exp_lvl')[['yearly_avg_salary']].mean()
# Percentage of postings with salary information
df.groupby('exp_lvl')[['yearly_avg_salary']].agg(lambda x: x.count()/(x.count()+x.isna().sum()))
# Average of availble salary rate at each level
df.groupby('exp_lvl')[['yearly_avg_salary']].mean()
# Median
df.groupby('exp_lvl')[['yearly_avg_salary']].median()

### NLP on job description
# Top 50 frequent unclean
jd_dict = df.full_description.str.split(expand=True).unstack().value_counts()
plot_data = [go.Bar(x=jd_dict.index.values[0:50],
                    y=jd_dict.values[0:50],
                    marker=dict(colorscale='Jet',
                               color=jd_dict.values[0:50]
                               ),
                    text='Word Counts')]
layout = go.Layout(title='Top 50 Frequent Words')                    
fig = go.Figure(data=plot_data, layout=layout)
py.plot(fig, filename='freq_bar')

### Word cloud
from wordcloud import WordCloud, STOPWORDS
stop_words = ['work', 'will', 'system', 'support'] + list(STOPWORDS)

# Word cloud for entry level job
jd_dict_1 = df[df.exp_lvl==1].full_description.values
j1_cloud = WordCloud(stopwords = stop_words,
                     background_color='white',
                     width=2500,
                     height=1800).generate(' '.join(jd_dict_1))
plt.imshow(j1_cloud)
plt.axis('off')

# Word cloud for mid level job
jd_dict_2 = df[df.exp_lvl==2].full_description.values
j2_cloud = WordCloud(stopwords = stop_words,
                     background_color='white',
                     width=2500,
                     height=1800).generate(' '.join(jd_dict_2))
plt.imshow(j2_cloud)
plt.axis('off')

# Word cloud for senior level job
jd_dict_3 = df[df.exp_lvl==3].full_description.values
j3_cloud = WordCloud(stopwords = stop_words,
                     background_color='white',
                     width=2500,
                     height=1800).generate(' '.join(jd_dict_3))
plt.imshow(j3_cloud)
plt.axis('off')