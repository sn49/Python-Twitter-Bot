import tweepy
from time import sleep
import datetime
import random

# Import Twitter credentials from credentials.py
from credentials import *


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

version = {"keyword_update": 0, "feature_update": 1, "error_fix": 2}


keyword_list = []

my_file = open("keyword.kwd", "r", encoding="UTF-8")
file_lines = my_file.readlines()
my_file.close()

# Create a for loop to iterate over file_lines
for line in file_lines:
    if "version=" in line:
        line = line.replace("\n", "")
        version["keyword_update"] = int(line.split("=")[1])
    else:
        keyword_list.append(line.replace("\n", ""))

print(keyword_list)
show_version = f"V=k{version['keyword_update']}-f{version['feature_update']}-e{version['error_fix']}"

api.update_profile(
    description=f"1시,5시,9시,13시,17시,21시 아무거나 대결 시키는 계정 | 비주기적으로 키워드 추가 | 현재 키워드 : {len(keyword_list)}개 | 버전 : {show_version}"
)

while True:
    # Add try ... except block to catch and output errors
    try:
        cnow = datetime.datetime.now()
        cmin = cnow.minute
        chour = cnow.hour

        if cmin == 0 and chour % 4 == 1:
            select_keyword = random.sample(keyword_list, 2)

            api.update_status(f"{select_keyword[0]} VS {select_keyword[1]}")
        else:
            print(f"{chour}시 {cmin}분")

    except tweepy.TwitterServerError as e:
        print(e.reason)
    sleep(60)
