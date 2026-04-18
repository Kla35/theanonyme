# Thé Anonyme - Un simple serveur Flask pour des message anonymisés ###

## Pourquoi ce projet ?

Parfois, une streameuse Twitch nommé AngleDroit fait des "sessions thés" sur ces lives, où les spectateurs lui envoient via son tchat Twitch des anecdotes de leurs vie, majoritairement à propos des relations. Ce système a quelques inconvénients. Le premier est de retrouver quels utilisateurs ont envoyés des messages, ainsi que tous les messages de l'utilisateur (surtout qu'il doit encore être là au moment de la lecture). La deuxième est que quelques spectateurs, puisque leurs comptes est connus par des proches, ne peuvent pas envoyer des anecdotes (comme la streameuse en question)

L'idée est que l'application conserve en mémoire vive, de manière donc éphémère les anecdotes. Pas de stockage autrement qu'en RAM, à la fin d'un stream, tout disparait.

Tout ce paragraphe pour dire que j'avais un peu de temps dans mes vacances, je voulais juste améliorer mes compétences en le faisant (et j'ai appris pas mal de choses sur Python Flask Server)

## Comment installer ?

* 1/ Clone le repository
* 2/ python3 -m venv .venv
* 3/ source .venv/bin/activate
* 4/ pip install -r requirements.txt
* 5/ cp .env.example .env
* 6/ Dans le fichier .env, changer les variables par vos valeurs
* 7/ python3 ./server.py

Le programme utilise le port 5000 par défaut

## Captures d'écran

![Screenshot Home](https://github.com/Kla35/theanonyme/blob/main/docs/screenshot_home.png)

![Screenshot Messages](https://github.com/Kla35/theanonyme/blob/main/docs/screenshot_messages.png)
--- 

# Thé Anonyme - Simple Flask server for anonymised message ###

## Why this project ?

Sometimes, a Twitch streamer called AngleDroit is doing some "tea time" or "gossip time" live, where viewers send via her Twitch chat some anecdote about their life, which are about relationship. There is some issue with this system. The first one is to find all messages of a user, limited by the length of Twitch message. The second one is where some users, because there accounts are known by friends, can't send their own anecdote (like the streamer herself).

The whole idea is in the app keep anecdotes in RAM, in a way it keep them ephemeral. No other stockage than RAM, at the end of a stream, all disappear.

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

## Screenshot

![Screenshot Home](https://github.com/Kla35/theanonyme/blob/main/docs/screenshot_home.png)

![Screenshot Messages](https://github.com/Kla35/theanonyme/blob/main/docs/screenshot_messages.png)

