# Thé Anonyme - Simple flask server for anonymised message ###

## Why this project ?

Sometimes, a Twitch streamer called AngleDroit is doing some "tea time" or "gossip time" live, where viewers send via her Twitch chat some anecdote about their life, which are about relationship. There is some issue with this system. The first one is to find all messages of a user, limited by the length of Twitch message. The second one is where some users, because there accounts are known by friends, can't send their own anecdote (like the streamer herself).

This whole paragraph just to tell I had some time on my hollyday, I just wanted to improve my skills by doing it (And I learned a lot of things about Python Flask Server)

## How to install ?

* 1/ Clone the repo
* 2/ python3 -m venv .venv
* 3/ source .venv/bin/activate
* 4/ pip install -r requirements.txt
* 5/ cp .env.example .env
* 6/ On .env, change all variables by your values
* 7/ python3 ./server.py

It will used by default the port 5000

