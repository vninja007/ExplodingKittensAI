# Exploding Kittens AI

This is my AI for Exploding Kittens. Currently, it has a 98% winrate against a random player, but the base strategy (a strategy that I use in my own play of Exploding Kittens, without any RL) has a 90% winrate. 

Code Structure:
- `/` is the directory for any reinforcement learning-related files. Although my code outputs policies into this folder, I"ve moved them all to `allpolicies/` for organization
- `allpolicies/` are different stages of the AI for Exploding Kittens, ranging from a 40% to a 98% win rate.
- `results/` contains mostly text files of different outputs that I've used to calculate statistics, such as the win rate in different scenarios of the game
- `ui/` is an *important folder*. It contains the actual UI where a user can play against my base version (the 90% win rate, not the 98% win rate AI). It operates off flask and can easily be set up by `python mainflask.py`. Note that flask must be installed.