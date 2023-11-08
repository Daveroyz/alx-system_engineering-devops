#!/usr/bin/python3
""" raddit api"""

import json
import requests

def count_words(subreddit, word_list, after=None, count_dict=None):
    if count_dict is None:
        count_dict = {}  # Initialize an empty dictionary to store the word counts
    
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "Recursive Reddit API Client"}

    params = {"limit": 100}  # Limit the number of posts per request
    if after:
        params["after"] = after

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        posts = data["data"]["children"]
        after = data["data"]["after"]

        for post in posts:
            title = post["data"]["title"].lower()
            for word in word_list:
                if word.lower() in title:
                    if word in count_dict:
                        count_dict[word] += 1
                    else:
                        count_dict[word] = 1

        if after:
            return count_words(subreddit, word_list, after, count_dict)
        else:
            sorted_counts = sorted(count_dict.items(), key=lambda x: (-x[1], x[0]))
            for word, count in sorted_counts:
                print(f"{word}: {count}")
    else:
        print("Error: Failed to fetch data from the Reddit API")

# Example usage:
count_words("python", ["reddit", "API", "python", "javascript"])
