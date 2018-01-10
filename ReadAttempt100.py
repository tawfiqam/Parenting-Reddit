
# coding: utf-8

# In[1]:

from __future__ import division, print_function
from bz2 import BZ2File
import ujson
from pandas import Timestamp, NaT, DataFrame
from toolz import dissoc
import cPickle
import numpy as np
import pandas as pd
import datetime
import dask.dataframe as dd
from dask.diagnostics import ProgressBar
pbar = ProgressBar()
pbar.register()
from pandas.io import sql
from castra import Castra
from toolz import peek, partition_all
import os
import glob
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import matplotlib.dates as mdates


columns = ['archived', 'author', 'author_flair_css_class', 'author_flair_text',
           'body', 'controversiality', 'created_utc', 'distinguished', 'downs',
           'edited', 'gilded', 'link_id', 'name', 'parent_id',
           'removal_reason', 'score', 'score_hidden', 'subreddit', 'ups']

final = []
path =r'/Users/tawfiq/Desktop/MyRedditFiles/CleanedJSONfiles/' # use your path

StartTime= str(datetime.utcnow())
print("starting to process cleaned yearly JSON files at "+ StartTime)
for f in glob.glob(path+"*.JSON"):
    with open(f, 'r') as jfile:
        for line in jfile:
            blob = ujson.loads(line)
            for i in range(0, len(blob)):
                date = blob[i]['created_utc']
                blob[i]['created_utc']= pd.to_datetime(date, unit='s')
                edited = blob[i]['edited']
                blob[i]['edited'] = pd.to_datetime(edited, unit='s') if edited else NaT
    
                # Convert deleted posts into `None`s (missing text data)
                if blob[i]['author'] == '[deleted]':
                    blob[i]['author'] = None
                if blob[i]['body'] == '[deleted]':
                    blob[i]['body'] = None
     
                final.append(dissoc(blob[i], 'id', 'subreddit_id', 'retrieved_on'))
                    
        FinishTime = str(datetime.utcnow())           
        print("processed "+str(len(blob))+" records from"+ f + "\n" + "at " + FinishTime + "\n")
    
RedditSub = pd.DataFrame.from_records(final, columns = columns)
RedditSub.set_index('created_utc')
RedditSub.head()


# In[2]:

pd.set_option('display.max_colwidth', -1)


# In[3]:

import praw

r = praw.Reddit('gettingpa')

child = r.get_info(thing_id='t3_1n9tme')


# In[4]:

def getFirstPost(link_id):
    child = r.get_info(thing_id= link_id)
    PostTitle = child.title
    PostUrl   = child.url
    PostText  = child.selftext
    Post = PostTitle + PostUrl + PostText
    return Post    


# In[5]:

RedditSub.sort_values(by=['created_utc'])


# In[6]:

len(RedditSub.index)


# In[7]:

SortedReddit = RedditSub.sort_values(by=['created_utc'])


# In[8]:

SortedReddit.groupby('link_id')


# In[14]:

SortedReddit.link_id.value_counts().nlargest(40)


# In[9]:

SortedReddit.subreddit.value_counts().nlargest(60)


# In[10]:

nothread = SortedReddit['link_id'].unique().tolist()
print("number of unique threads")
len(nothread)


# In[11]:

unique_users=RedditSub['author'].unique().tolist()   #getting a list of unique authors on all parenting reddits
print("length before None removed ")
len(unique_users)


# In[12]:

#filter out None value if exists
unique_users = filter(None,unique_users)
print("length after  None removed ")
len(unique_users)


# In[13]:

RedditSubGroups=SortedReddit.groupby('subreddit') #group your dataframe according to a specific column, here, the subreddit


# In[14]:

unique_subreddit=RedditSub['subreddit'].unique().tolist()   #getting a list of subreddits re parenting (37)
print("Number of subreddits that talk about parenting ")
len(unique_subreddit)


# In[15]:

unique_subreddits = SortedReddit['subreddit'].unique().tolist()   #get a list of subreddits
print(unique_subreddits)


# In[16]:

dataframelist=[]
for sub in unique_subreddits:
    df = RedditSubGroups.get_group(sub)
    dataframelist.append(df)


# In[17]:

for subreddit in unique_subreddits:
    for i in range(0,36):
        subreddit = pd.DataFrame(dataframelist[i])


# In[18]:

Parenting = dataframelist[0]
Adoption = dataframelist[1]
SingleParents = dataframelist[2]
Daddit = dataframelist[3]
RadicalParenting= dataframelist[4]
Parentsfrommultiple = dataframelist[5]
Pregnant= dataframelist[6]
TroubledTeeds = dataframelist[7]
AttachmentParenting = dataframelist[8]
Homeschool = dataframelist[9]
Breastfeeding = dataframelist[10]
NewParents = dataframelist[11]
BabyExchange = dataframelist[12]
Parent = dataframelist[13]
Tryingforbaby = dataframelist[14]
Familydinner = dataframelist[15]
Samesexparents = dataframelist[16]
Stepparents = dataframelist[17]
Predaddit = dataframelist[18]
SpecialNeedsChildren = dataframelist[19]
Pottytraining = dataframelist[20]
ParentingLite = dataframelist[21]
Birthparents = dataframelist[22]
RaisedbyNarcessists= dataframelist[23]
ScienceParents=dataframelist[24]
Kidscrats = dataframelist[25]
Breakingmom = dataframelist[26]
Badparenting=dataframelist[27]
Mombloggers = dataframelist[28]
Internetparents = dataframelist[29]
AsianParentStories = dataframelist[30]
TrollXMoms = dataframelist[31]
Entitledparents = dataframelist[32]
Badparents = dataframelist[33]
Parentingfails = dataframelist[34]
Beetlejuicing = dataframelist[35]
AngrySportingParents= dataframelist[36]


# In[19]:

Parenting.head(100)


# In[20]:

Parenting.link_id.value_counts().nlargest(40)


# In[21]:

Parenting[Parenting['link_id'] == 't3_1n9tme'].head(300)


# In[22]:

Vaccines = Parenting[Parenting['link_id'] == 't3_1n9tme']


# In[23]:

#ReadingBody
PostTitle = child.title
PostUrl   = child.url
PostText  = child.selftext
Post = PostTitle + PostUrl + PostText
cleanedbody=Vaccines['body'].fillna('')
bodylist = cleanedbody.tolist()
body = ' '.join(bodylist)
body= body.encode('utf-8').strip()
with open("Vaccines.txt", "w") as text_file:
    text_file.write(Post)
    text_file.write(body)


# In[24]:

Parenting.head(100)


# In[25]:

Parenting[Parenting['link_id'] == 't3_6d8mh'].head(300)


# In[26]:

nothread = Breakingmom['link_id'].unique().tolist()
listID = ','.join(nothread)
listID = listID.encode('utf-8').strip()
print("the list of ids")
print(listID)
print("number of unique threads")
len(nothread)


# In[27]:

user = r.get_redditor('avinassh')
print(user.created_utc)
print(user.get_multireddits)
print(user.get_multireddit)
print(user.is_friend)
print(user.is_mod)


# In[30]:

Parenting = Parenting.set_index(Parenting.created_utc)


# In[31]:

cnt = Parenting.groupby(Parenting.index.year)['author'].nunique()


# In[32]:

print(cnt)


# In[36]:

import statsmodels.api as sm
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

monthly = Parenting

years = mdates.YearLocator()
months = mdates.MonthLocator()
yearsFmt = mdates.DateFormatter('%Y')

fig, zx = plt.subplots()
ax.plot(monthly.created_utc)

ax.format_ydata = mdates.DateFormatter('%Y-%m-%d')
ax.format_xdata = mdates.monthly.controversiality
ax.grid(True)

decomp = monthly.groupby(pd.TimeGrouper("M")).mean()
fig.autofmt_xdate()
decomp.plot()
plt.show()


# In[35]:

import statsmodels.api as sm
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
yearsFmt = mdates.DateFormatter('%Y')


fig, ax = plt.subplots()
ax.plot(monthly.created_utc)

ax.format_ydata = mdates.DateFormatter('%Y-%m-%d')
ax.format_xdata = monthly.controversiality
ax.grid(True)

decomp = monthly.groupby(pd.TimeGrouper("M")).mean()
fig.autofmt_xdate()
decomp.plot()
plt.show()

#g = Parenting.groupby(pd.TimeGrouper("M"))
#g.sum()


# In[64]:

g = Parenting['score']
z = Daddit['score']
g = Parenting.groupby(pd.TimeGrouper("M"))
g.sum()
g.mean()
z.mean()


# In[59]:

# Graphing MAU
import statsmodels.api as sm
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
yearsFmt = mdates.DateFormatter('%Y')

monthly = Parenting

fig, ax = plt.subplots()
ax.plot(monthly.created_utc)

ax.format_ydata = mdates.DateFormatter('%Y-%m-%d')
ax.format_xdata = monthly.score
ax.grid(True)


#decomp = monthly.groupby(monthly.index.date)['author'].nunique()

decomp =  monthly.groupby(monthly.created_utc)['author'].nunique()


fig.autofmt_xdate()
decomp.plot()
plt.show()

#print(monthly.groupby(monthly.index.date)['author'].nunique())


# In[ ]:

from __future__ import print_function
import pandas as pd
import matplotlib.pyplot as plt

import statsmodels.api as sm


# In[ ]:

fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)
dta.realgdp.plot(ax=ax);
legend = ax.legend(loc = 'upper left');
import matplotlib.pyplot as plt
import numpy as np
import datetime as dtlegend.prop.set_size(20);


# In[66]:

ig, (ax1, ax2) = plt.subplots(nrows = 2, sharex = True)
#ig, ax1
ax1.format_ydata = mdates.DateFormatter('%Y-%m-%d')
ax2.format_ydata = mdates.DateFormatter('%Y-%m-%d')
ax1.plot(g.mean())
ax2.plot(z.mean())
#ax2.plot(Parenting.ups)

plt.show()


# In[ ]:



