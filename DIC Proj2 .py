#!/usr/bin/env python
# coding: utf-8

# # Collecting NYTimes data for topic : Sports

# In[3]:


from nytimesarticle import articleAPI
from bs4 import BeautifulSoup
import requests
import time
api = articleAPI("5zyZtAbijJdB21cuSw0UvUTUmyJfE7G8")



words = ['Soccer','Swimming','Basketball','Golf','Tennis']   #Sub-topics
try:
    for word in words:
        articles = []
        print(word)
        for a in range(0,25):
            time.sleep(10)
            data = api.search(q= word, begin_date=20190101,end_date=20190414,page=a)
            for i in range(0,len(data['response']['docs'])):
                url = data['response']['docs'][i]['web_url']
                r = requests.get(url)
                soup = BeautifulSoup(r.content, 'html.parser')
                soup.prettify()
                file =open('/Users/aniket/Documents/HadoopData/NewYorkTimesData/NYT-'+word+'.txt','a+')
                for j in range((len(soup.find_all('p')))-3):
                    file.write(soup.find_all('p')[j].get_text())
                
                articles.append(url)
        print('Number of articles for '+word+ ' obtained are :',len(articles))
        file.close()

except:
    print("Number of articles only ",len(articles))


# In[21]:


#Now we merge all the above text files into one big text file.
import glob
import os
os.chdir("/Users/aniket/Documents/HadoopData/NewYorkTimesData")
filenames = glob.glob("*.txt")

with open('/Users/aniket/Documents/HadoopData/NewYorkTimesData/AllSportsNYT.txt', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)


# Collecting Twitter data for topic : Sports

# In[6]:


import tweepy
import csv
import pandas as pd

api_key = "TfNOdi7WVi9Et3xKXDY4q35m8"
api_secret = "JMR4Cz2sZXdPjFhlZmNhd6ULJf5Vxnh6WzUNS6zVHwJcSNCN18"
access = "1039892313823227906-DAVrNAPNZkX2QJOffEf6InWCCIZePL"
access_secret = "QxOVJCTUwhwLf1EmanwluwdqGYfi08LlgpQA0A0znHrs4"

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access, access_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
Total_count = []
words = ['Soccer','Swimming','Basketball','Golf','Tennis']   #Sub-topics
for word in words:
    print(word)
    csvFile = open('/Users/aniket/Documents/HadoopData/TwitterData/Tweet-'+word+'.csv', 'a')
    csvWriter = csv.writer(csvFile)
    count = 0
    for tweet in tweepy.Cursor(api.search,q= word,
                               tweet_mode='extended',lang="en",
                               since="2019-01-01").items(20000):
        if (not tweet.retweeted) and ('RT @' not in tweet.full_text):
            count +=1
            print(count)
            csvWriter.writerow([tweet.full_text.encode('utf-8')])
    Total_count.append(count)
    csvFile.close()
    print('The following subtopic is done :',word)



# In[8]:


print(sum(Total_count))


# In[18]:


#Now we merge the above csv files into one big csv file.
import glob
import os
os.chdir("/Users/aniket/Documents/HadoopData/TwitterData")
fileList = glob.glob("*.csv")
combined_csv = pd.concat( [ pd.read_csv(f) for f in fileList ] ,axis = 0)
combined_csv.to_csv( "/Users/aniket/Documents/HadoopData/TwitterData/AllSports.csv", index=False )


# In[22]:


# Now we convert the csv files to text file for the purpose of this project.

with open("/Users/aniket/Documents/HadoopData/TwitterData/AllSports.txt", "w") as my_output_file:
    with open("/Users/aniket/Documents/HadoopData/TwitterData/AllSports.csv", "r") as my_input_file:
        [ my_output_file.write(" ".join(row)+'\n') for row in csv.reader(my_input_file)]
    my_output_file.close()


# # Now we begin cleaning data

# In[265]:


import re
import regex
with open('/Users/aniket/Documents/HadoopData/TwitterData/AllSports.txt', 'r') as file:
    data = file.read().replace('\n', '')
line = (re.sub('(RT )*@.+? ', '',data)) # dont want <RT and/or @user> tags
line = (re.sub('http.+? ', '',line)) # dont want web adresses
line = re.sub(',', ' ', line)
line = line.lower()
words = re.findall('([a-z]+?.{0,1}?[a-z]*?)\W*\s+',line)


# In[266]:


from nltk.stem import WordNetLemmatizer 
  
alpha = []
lemmatizer = WordNetLemmatizer() 
for i in words:  
    n = lemmatizer.lemmatize(i,pos = 'v') 
    alpha.append(n)


# In[294]:


from nltk.corpus import stopwords 

stop_words = set(stopwords.words('english'))
stop_words.add('would')
stop_words.add('go')
stop_words.add('get')
stop_words.add('say')
stop_words.add('make')
stop_words.add('like')
stop_words.add('also')
new_alpha = []
for i in alpha:
    if i not in stop_words:
        new_alpha.append(i)


# In[306]:


new_new_alpha = []
for i in new_alpha:
    if i.isalpha() == True:
        new_new_alpha.append(i)

omega = ''
for i in new_new_alpha:
    omega += i + ' '


# In[307]:


file = open('/Users/aniket/Documents/HadoopData/TwitterData/LatestTweets.txt','w')
file.write(omega)
file.close()


# In[325]:


# Now let's start with NYT
import re
import regex
with open('/Users/aniket/Documents/HadoopData/NewYorkTimesData/AllSportsNYT.txt', 'r') as file:
    data = file.read().replace('\n', '')


# In[326]:


from nltk.stem import WordNetLemmatizer 
from nltk.tokenize import sent_tokenize, word_tokenize
nex = word_tokenize(data)
  
alpha = []
lemmatizer = WordNetLemmatizer() 
for i in nex:  
    n = lemmatizer.lemmatize(i,pos = 'v') 
    alpha.append(n)


# In[327]:


beta = ''
for i in alpha:
    beta += i + ' '


# In[328]:


line = (re.sub('(RT )*@.+? ', '',beta)) # dont want <RT and/or @user> tags
line = (re.sub('http.+? ', '',line)) # dont want web adresses
line = re.sub(',', ' ', line)
line = line.lower()
words = re.findall('([a-z]+?.{0,1}?[a-z]*?)\W*\s+',line) # regex to extract words (space delmit, remove special chars at end of words)


# In[329]:



new_words = []
for i in words:
    if i not in stop_words:
        new_words.append(i)


# In[330]:


new_new_words = []
for i in new_words:
    if i.isalpha() == True:
        new_new_words.append(i)

beta = ''
for i in new_new_words:
    beta += i + ' '
file = open('/Users/aniket/Documents/HadoopData/NewYorkTimesData/LatestNY.txt','w')
file.write(beta)
file.close()


# In[334]:


import pandas as pd
df1 = pd.read_csv('/Users/aniket/Documents/HadoopData/NY.txt', sep="\t", header=None)
df1.columns = ["word", "count"]
Top_ten_NYT = df1.sort_values(by=['count'])
Top_ten_NYT.tail(11)


# In[323]:


import pandas as pd
df2 = pd.read_csv('/Users/aniket/Documents/HadoopData/TW.txt', sep="\t", header=None)
df2.columns = ["word", "count"]
Top_ten_Twitter = df2.sort_values(by=['count'])


# In[324]:


Top_ten_Twitter.tail(10)


# In[337]:


Top_ten_Twitter.tail(10).to_csv('/Users/aniket/Documents/HadoopData/Top-ten-twitter.csv',index = False)


# In[338]:


Top_ten_NYT.tail(10).to_csv('/Users/aniket/Documents/HadoopData/Top-ten-NYT.csv',index = False)


# In[ ]:




