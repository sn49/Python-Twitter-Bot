import os
import tweepy
from time import sleep
import datetime
import random

# Import Twitter credentials from credentials.py
from credentials import *


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

version = {"keyword_update": 0, "feature_update": 2, "error_fix": 3}
show_version = f"V=k{version['keyword_update']}-f{version['feature_update']}-e{version['error_fix']}"

keyword_list = []


def update_sv():
    global show_version
    show_version = f"V=k{version['keyword_update']}-f{version['feature_update']}-e{version['error_fix']}"


def twitter_up(descript):
    api.update_profile(description=descript)


def update_wordlist():
    global version
    global keyword_list
    keyword_list.clear()

    my_file = open("keyword.kwd", "r", encoding="UTF-8")
    file_lines = my_file.readlines()
    my_file.close()

    for line in file_lines:
        if "version=" in line:
            line = line.replace("\n", "")
            version["keyword_update"] = int(line.split("=")[1])
        else:
            one_word = line.replace("\n", "")
            if not one_word == "":
                keyword_list.append(one_word)
            print(keyword_list)
    update_sv()
    twitter_up(
        f"홀수시에 아무거나 대결 시키는 계정 | 비주기적으로 키워드 추가 | 현재 키워드 : {len(keyword_list)}개 | 버전 : {show_version}"
    )


update_wordlist()


while True:
    # Add try ... except block to catch and output errors
    try:
        cnow = datetime.datetime.now()
        cmin = cnow.minute
        chour = cnow.hour

        if cmin == 0 and chour % 2 == 1:
            select_keyword = random.sample(keyword_list, 2)

            api.update_status(f"{select_keyword[0]} VS {select_keyword[1]}")
        else:
            if os.path.exists("goupdate.txt"):
                if open("goupdate.txt", "r").read() == "Update WordList":
                    update_wordlist()
            print(f"{chour}시 {cmin}분")

    except tweepy.TwitterServerError as e:
        print(e.reason)
    sleep(60)
