#!/bin/bash

# Start prodigy app for text classification annotations
# Storing in 'tweet_identification_filtered' SQLite data base, reading tweets from 'oupt_tweets_filtered.jsonl' file, annotating for statuses and news
python -m prodigy textcat.manual tweet_identification_filtered oupt_tweets_filtered.jsonl --label status,news
