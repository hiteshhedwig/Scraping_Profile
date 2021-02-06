"""
TASK ONE : Write a program to scrap a data for last 3 months 
from online profile for example 
- Twitter, StackOverflow, GItHub 
( Use your profile as of now for testing)
"""
import datetime as dt
import pandas as pd 
import sys, tweepy
import argparse
import time
from datetime import timedelta
import urllib
from bs4 import BeautifulSoup
import sys
import csv
import json
import os
import shutil

parser= argparse.ArgumentParser(description='Web Scraping')
parser.add_argument('--twitter', type=bool, default=False,
                    choices=[True, False])
parser.add_argument('--github', type=bool, default=False,
                    choices=[True, False])
#parser.add_argument('--github', type=bool, default=False,choices=[True, False])

class ScrapTwitter():

    def __init__(self, username):

            self.consumer_key='jsul297h8ZDM9iGNI6iXkZPBs'
            self.consumer_secret='obNC5dy5HeQyfM849DpaJxwTeULtMgHVKL2szg9hiH1yieFzjj'
            self.access_token= '315632565-tvZG2BdtN97FHBxoy7JL4HgDvVbIk0Tjnq9jUeI9'
            self.access_secret= 'TEWB9EnfeHxyM2MB56IsiKpWpIKuaAEyv8vNXLzhufwrr'
            self.username= username
            self.api= self.get_twitter_client()
            

    def get_twitter_client(self):
        
        auth= self.auth_verify()
        client= tweepy.API(auth, wait_on_rate_limit= True)
        return client


    def auth_verify(self):
        
        auth= tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token,self.access_secret)

        return auth

    def get_dataset(self):
        
        count = 150

        try:     
            # Creation of query method using parameters
            api=self.api
            tweets = tweepy.Cursor(api.user_timeline,id=self.username).items(count)
                

            tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]
            
            # Creation of dataframe from tweets list
            # Add or remove columns as you remove tweet information
            tweets_df = pd.DataFrame(tweets_list, columns=['Time','Id','Tweet'])
            
            tweets_df= self.last_threemonth_records(tweets_df)
            tweets_df.to_csv(f'{self.username}_twitter.csv', header=tweets_df.columns)
            

            return tweets_df
            
        except BaseException as e:
            raise NameError('Username may not be correct. Please, double check')
            time.sleep(3) 
        

    def last_threemonth_records(self, df):
        last_3_months= df.Time[0]-timedelta(days=90)
        return df[df.Time>last_3_months]

class GitHubScrap():

  def __init__(self, username):
    self.username= username
    self.url = 'http://github.com/' + username
    self.data = urllib.request.urlopen(self.url).read()
    self.soup = BeautifulSoup(self.data,"html.parser")

  def gather_data(self):
    f = open(self.username + '.csv', 'wt')
    days = self.soup.findAll('rect', {'class' : 'day'})
    writer = csv.writer(f)
    writer.writerow(('Commit Count', 'Date'))

    for day in days:
        count = day['data-count']
        date = day['data-date']
        writer.writerow((count,date))

    f.close()

    df= pd.read_csv(f'{self.username}.csv')

    return df

  def json_data(self):
      ### get profile info
        fullname = self.soup.find('span', {'class' : 'vcard-fullname'}).string
        username = self.soup.find('span', {'class' : 'vcard-username'}).string
        followers = self.soup.find('span', {'class' : 'text-bold text-gray-dark'}).string
        last_year_contrib = self.soup.find('h2', {'class' : 'f4 text-normal mb-2'}).string.strip().split(' ')[0]
        repos = self.soup.findAll('span', {'class' : 'repo'})
        reposi=[]
        for i in repos:
                pop= i['title']
                reposi.append(pop)
        output=[]
        output.append({'full name': fullname, 'user name': username, 'followers': followers, 
                    'popular repo': reposi, 'last_year_contributions': last_year_contrib})

        with open(self.username + ".json", "w") as outputfile:
            json.dump(output, outputfile, indent=2)
            #print ('dumping ', outputfile)
       

    
  def records(self, df):
        df_ext=df.copy()
        df_ext.Date =  pd.to_datetime(df_ext.Date, infer_datetime_format=True)
        last_3_months= df_ext.Date[len(df_ext)-1]-timedelta(days=90)
        return df_ext[df_ext.Date>last_3_months]


if __name__ == '__main__':
    args= parser.parse_args()

    if args.twitter:
        username= str(input("Enter Twitter username : "))
        twitter= ScrapTwitter(username)
        dataset= twitter.get_dataset()
        #print(dataset)   

    
    if args.github:
        username= str(input("Enter Github username : "))
        github= GitHubScrap(username)
        data= github.gather_data()
        data_extracted= github.records(data)
        github.json_data() #profile data



