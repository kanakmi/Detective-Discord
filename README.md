# Detetective Discord

## 💡 Inspiration
Have you ever recieved a message like this?

<p align="center">
<img width="30%" src="https://user-images.githubusercontent.com/54859521/150679129-0ac89bbb-6a90-43e4-96a5-c248b57e5544.png"/> <img width="31%" src="https://user-images.githubusercontent.com/54859521/150679357-43aa6388-4679-4a7b-b390-09a1cdba5508.png" />
</p>

If you have been on Discord for a while, I am sure you have been warned to stay away from these links. <br>
But what about the newbies that are just starting out? <br>
One of such incidents happend this thursday on my server. A bunch of people fell victim to such phishing links. <br>
There was no such bots available in the market to solve this problem so I decided to make it on my own. <br>

## 💻 What it does
Detective Discord is a bot that detects phishing links in Discord messages, deletes them, warns the user who sent them and increase thier warning count by 1. Once the warning count reaches 3, the user is banned from the server. <br>
In case of a ban, the user is also informed by the bot for the same. <br>

This bot can also perform a few other actions like:
- $news - Get latest news from BBC
- $weather <city> - Get weather in a city
- $joke - Get a random joke
- $wiki <search key> - Get a summary of a search key from Wikipedia
- $help - Get this message
- $reset_warn <user> - Reset warnings for a user (admin/moderator only)

## ⚙️ How I built it
The rules to detect phishing links are simple:
- Check if the message contains a link.
- Check if the link is not exactly the same as the real discord links like *discord.gg* or *discord.me*.
- Calculate the Levenstien Distance between the link and the real discord links.
- If the distance is less than 4, or the message contains words like *discord* or *nitro*, the link is considered to be phishing link.

For fetching the News, the bot uses the BBC API. <br>
For fetching the weather, the bot uses the OpenWeatherMap API. <br>
For fetching the jokes, the bot uses the pyjokes python library. <br>
For fetching the Wikipedia summary, the bot uses the Wikipedia python library. <br>
  
## ⚙️ Tech Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Discord](https://img.shields.io/badge/Discord.py-%237289DA.svg?style=for-the-badge&logo=discord&logoColor=white) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) ![Wikipedia](https://img.shields.io/badge/Wikipedia-%23000000.svg?style=for-the-badge&logo=wikipedia&logoColor=white) 

## 🧠 Challenges we ran into
At first, I thought it would be a really simple task but as I started to build it, I realized it wasn't that easy after all. <br>
Firstly I had to make the rules to identify phishing links. But I also had to make sure that the bot would not delete the links that are not phishing links. <br>
After hovering over various methods, I settled on using the Levenstien Distance algorithm. <br>
After that, when testing the bot I realized that the bot would also delete the links that were not phishing links but other discord links. <br>
So I had to tweak the rules and make them inclusive to the other links. <br>
Finally, I had a hard time deleting the user from the database who sent the phishing links. There was a bug that I wasn't able to detect and it took me 1 whole hour to fix it. <br>

## 🏅 Accomplishments that we're proud of
I am proud of the fact that I was able to build this bot in a day and that now my Server will no longer suffer from these phishing scams.

## 📖 What we learned
This is the first time I have build a discord bot. I learnd how to use the discord.py library and how to use the discord.py API. <br>

## 🚀 What's next for Detetective Discord
Setting a workflow to save the phishing links in the database and at the stroke of the midnight, report them through the appropriate channels. <br>
