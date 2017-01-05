
# coding: utf-8
"""
    A dump of the jupyter notebook. Use the notebook if possible. It's much more readable.
"""
# ### Goals: 
# * Time in match
# * Time to find match
# 

# In[2]:

import os
import sys
import json
import pandas as pd
import math
import matplotlib.pyplot as plt
from datetime import datetime
import time
import matplotlib.dates as mdates

get_ipython().magic(u'matplotlib inline')

def extract_date(data):
    return data_date
    x = data["match_completed"]["ts"]
    first_i = x.first_valid_index()
    last_i = x.last_valid_index()
    first_date = datetime.fromtimestamp(int(x[first_i])/1000.0)
    last_date = datetime.fromtimestamp(int(x[last_i])/1000.0)
    mid = first_date + (last_date - first_date)/2
    return str(mid.date())

def read_data_multiple(path_label_tuples):
    data = {label:read_data(path) for path, label in path_label_tuples}

def expand_custom_params(outer_data, custom_event_name):
    inner_data = (pd.DataFrame(outer_data["custom_params"].tolist())) 
    joined = pd.DataFrame.merge(outer_data, inner_data, left_index=True, right_index=True)
    return joined.drop("custom_params", 1)

def read_data(path):
    custom_data = ""
    with open(path) as f:
        decoder = json.JSONDecoder()
        data = [decoder.decode(line) for line in f.readlines()]
        frame = pd.DataFrame(data)
        custom_data = {name:expand_custom_params(frame[frame["name"] == name], name) for name in pd.unique(frame["name"])}
    return custom_data


# In[ ]:


data_dates = [
    "9-20-2016", 
    "9-21-2016", 
    "9-22-2016", 
    "9-23-2016", 
    "9-24-2016", 
    "9-25-2016", 
    "9-26-2016", 
    "9-27-2016", 
    "9-28-2016", 
    "9-29-2016", 
    "9-30-2016",
    "10-1-2016", 
    "10-2-2016", 
    "10-3-2016", 
    "10-4-2016", 
    "10-5-2016", 
    "10-6-2016", 
    "10-7-2016", 
    "10-8-2016", 
]

data = []
dates = []
print "preparing to process" 
for date_string in data_dates:
    fp = "C:/Users/jephron/Downloads/unity_analytics_results/{}.json".format(date_string)
    custom_data = read_data(fp)
    date = datetime.strptime(date_string, "%m-%d-%Y").date()
    dates.append(date)
    data.append(custom_data)
    print "processed", date
    
#     wait_times = custom_data["match_made"]["time_waited"].apply(float)
#     print d, "mean wait time", wait_times.mean(), "seconds"
#     print d, "median wait time", wait_times.median(),"seconds"
#     print d, "maximum wait time", wait_times.max(),"seconds"
#     print d, "min wait time", wait_times.min(),"seconds"
#     wait_data.append(wait_times)
    
#     match_lengths = custom_data["match_completed"]["time_remaining"].apply(float).apply(lambda x : 60-x).where(lambda x : x < 60)
# #     print d, "mean match length ", match_lengths.mean(), "seconds"
# #     print d, "median match length ", match_lengths.median(),"seconds"
# #     print d, "maximum match length ", match_lengths.max(),"seconds"
# #     print d, "min match time ", match_lengths.min(),"seconds"
#     match_length_data.append(match_lengths)
    
#     kos = custom_data["match_completed"][(custom_data["match_completed"]["win_state"] == "Win_ko") | (custom_data["match_completed"]["win_state"] == "WinStreak_ko")]
    
#     ko_data.append(kos)
#     

# filepath = "C:/Users/jephron/Downloads/unity_analytics_results/{}.json".format("9-20-2016")


# multi = [("C:/Users/jephron/Downloads/unity_analytics_results/9-24-2016.json", "9-24-2016"),
#          ("C:/Users/jephron/Downloads/unity_analytics_results/9-23-2016.json", "9-23-2016"),
#          ("C:/Users/jephron/Downloads/unity_analytics_results/9-22-2016.json", "9-22-2016")]

# multidata = read_data_multiple(multi)

# custom_data = read_data(filepath)


# In[99]:

means = map(lambda x : x.mean(), wait_data)
medians = map(lambda x : x.median(), wait_data)
maxes = map(lambda x : x.max(), wait_data)
mins = map(lambda x : x.min(), wait_data)

fig, ax = plt.subplots(1)
plt.title("wait times")
ax.set_ylabel('time (s)')

pltmeans, = plt.plot(dates, means)
pltmedians, = plt.plot(dates, medians)
lgd = plt.legend([pltmeans, pltmedians], ['Mean', 'Median'], bbox_to_anchor=(1.05, 1), loc=2)
fig.autofmt_xdate()
yearsFmt = mdates.DateFormatter('%m/%d')
days = mdates.DayLocator()
ax.xaxis.set_major_formatter(yearsFmt)
ax.xaxis.set_major_locator(days)
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 15
fig_size[1] = 9
plt.rcParams["figure.figsize"] = fig_size
plt.show()
fig.savefig("./out/waitstimes.png", dpi=200, bbox_extra_artists=(lgd,), bbox_inches='tight')


# In[5]:

means = map(lambda x : x.mean(), match_length_data)
medians = map(lambda x : x.median(), match_length_data)
maxes = map(lambda x : x.max(), match_length_data)
mins = map(lambda x : x.min(), match_length_data)

fig, ax = plt.subplots(1)
plt.title("Match Lengths")
ax.set_ylabel('Time spent in match (s)')

pltmeans, = plt.plot(dates, means)
pltmedians, = plt.plot(dates, medians)
lgd = plt.legend([pltmeans, pltmedians], ['Mean', 'Median'], bbox_to_anchor=(1.05, 1), loc=2)
fig.autofmt_xdate()
yearsFmt = mdates.DateFormatter('%m/%d')
days = mdates.DayLocator()
ax.xaxis.set_major_formatter(yearsFmt)
ax.xaxis.set_major_locator(days)
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 15
fig_size[1] = 9
plt.rcParams["figure.figsize"] = fig_size
plt.show()
fig.savefig("./out/match_lengths.png", dpi=200, bbox_extra_artists=(lgd,), bbox_inches='tight')


# In[23]:

num_matches = map(len, match_length_data)


fig, ax = plt.subplots(1)
plt.title("Matches played and Knockouts")
ax.set_ylabel('Count')

pltmatches, = plt.plot(dates, num_matches)
pltkos, = plt.plot(dates, map(len, ko_data))
lgd = plt.legend([pltmatches, pltkos], ['Matches', 'KOs'], bbox_to_anchor=(1.05, 1), loc=2)

fig.autofmt_xdate()
yearsFmt = mdates.DateFormatter('%m/%d')
days = mdates.DayLocator()
ax.xaxis.set_major_formatter(yearsFmt)
ax.xaxis.set_major_locator(days)
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 15
fig_size[1] = 9
plt.rcParams["figure.figsize"] = fig_size
plt.show()
fig.savefig("./out/KOs_plus_matches.png", dpi=200)


# In[ ]:




# In[ ]:

wait_times = custom_data["match_made"]["time_waited"].apply(float)
print d, wait_times.mean()
print d, wait_times.median()

matches_completed = custom_data["match_completed"]
matches_completed["player_rank"] = matches_completed["player_rank"].apply(float)
matches_completed["player_score"] = matches_completed["player_score"].apply(float)

z = matches_completed["time_remaining"].apply(float)

def gen_header(title):
    formatted = "d={} : {} : n={}".format(extract_date(custom_data), title, str(len(matches_completed)))
    return formatted

def gen_filename(title):
    formatted = "./out/{}_{}.png".format(extract_date(custom_data), title)
    return formatted

plt = z[z>=0].plot.hist(alpha=0.5, 
                  title=gen_header("match time remaining"), 
                  figsize=(15,10)).set(xlabel="Time remaining (s)")

plt[0].get_figure().savefig(gen_filename("match_time_remaining"))

custom_data["match_made"]["time_waited"] = custom_data["match_made"]["time_waited"].apply(float)
custom_data["match_made"]["player_rank"] = custom_data["match_made"]["player_rank"].apply(float)
plt = custom_data["match_made"].plot.scatter(
    title=gen_header("time waited vs player rank"), 
    y="time_waited", 
    x="player_rank", 
    figsize = (15,10))

plt.get_figure().savefig(gen_filename("time_waited"))


# In[13]:




# In[ ]:

matches_made = custom_data["match_made"]
# matches_made["time_waited"].apply(float).plot.hist()
#


# In[ ]:

matches_made["time_waited"].apply(float).plot.hist


# In[ ]:




# In[10]:

a = [1,2,3,4,5,6]
a.append


# In[ ]:



