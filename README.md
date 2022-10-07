![GitHub Socialify](https://socialify.git.ci/kanakmi/Detective-Discord/image?description=1&forks=1&issues=1&language=1&name=1&owner=1&pattern=Plus&pulls=1&stargazers=1&theme=Dark)

## 💡 Innovation of the bot

Have you ever got notified by a message like this?

<p align="center">
<img width="30%" src="https://user-images.githubusercontent.com/54859521/150679129-0ac89bbb-6a90-43e4-96a5-c248b57e5544.png"/> <img width="31%" src="https://user-images.githubusercontent.com/54859521/150679357-43aa6388-4679-4a7b-b390-09a1cdba5508.png" />
</p>

If you have been on Discord for a while, I am sure you have been warned to stay away from these links. <br>
But the newcomers out there don't have any idea about these links and fall into such scams and loose access to their discord accounts.

## 💻 What it does ?

It's a bot that detects phishing links in discord messages, deletes them, warns the user who sent them and increase thier warning count by 1. Once the warning count hits 3, the user is kicked from the server and the user is also informed by the bot. <br>
When the user is, the user is also informed by the bot for the same. <br>

![Member Kicked](https://user-images.githubusercontent.com/54859521/194545745-3b880a6a-e91e-499d-a797-1c96ab5528ac.png)

If the bot is unable to delete the message due to missing permissions (not every server admin allows the bot to delete server messages), it replies to the message - <br>

![image](https://user-images.githubusercontent.com/54859521/194545318-c766d6b7-e87b-4f0c-84b0-71ed19e105f4.png)

This way, it alerts the members of the server untill the Moderators eventually delete the message.

#### Some of the bot actions:

- `/wiki` - Returns a Wikipedia summary

![wiki](https://user-images.githubusercontent.com/54859521/194546793-f4339a0c-0f54-4c4c-bc66-11df5adffe04.png)

- `/joke` - Returns a random joke

![joke](https://user-images.githubusercontent.com/54859521/194547247-661d59fa-d52d-4e86-a22c-bdaa13221e69.png)

- `/news` - Returns the top 5 news from BBC

![news](https://user-images.githubusercontent.com/54859521/194547431-b9d3bfb9-25d7-44d9-86d2-b04f9a19eb24.png)

- `/weather` - Returns the weather of a city

![weather](https://user-images.githubusercontent.com/54859521/194547554-817f4983-e4c2-4765-b2e4-272a6c786282.png)

- `/help` - Returns all the commands that the bot supports

#### Admin/Mod commands

- `/reset_warn` - Reset warnings for a member

![reset_warn](https://user-images.githubusercontent.com/54859521/194548071-43cecee9-a221-4cab-91de-1281403f5ab9.png)

- `/safe_domain` - Add a domain to the safe domains list

![image](https://user-images.githubusercontent.com/54859521/194548279-ce6002ea-1765-4803-a1dd-f79ed6941f7c.png)

- `/unsafe_domain` - Remove a domain from the safe domains list

![image](https://user-images.githubusercontent.com/54859521/194548588-a38f0a03-1935-4a63-9cdf-339af7881314.png)

## ⚙️ Logic for Phishing Link detection

The rules to detect phishing links are quite simple:

- If the message includes any link
- Check if the link is not included in the safe domains list (stored in domains.db). Current links include _discord.gift, discord.com, discord.gg, discord.me, discord.io, discordapp.com_.
- Calculate the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) between the message link and the real discord links.
- If the distance is less than 5, the link is considered to be dangerous link.

For fetching the News, the bot uses the BBC API. <br>
For fetching the weather, the bot uses the OpenWeatherMap API. <br>
For fetching the jokes, the bot uses the pyjokes python library. <br>
For fetching the Wikipedia summary, the bot uses the Wikipedia python library. <br>

## ⚙️ Tech Stack

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Discord](https://img.shields.io/badge/Discord.py-%237289DA.svg?style=for-the-badge&logo=discord&logoColor=white) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) ![Wikipedia](https://img.shields.io/badge/Wikipedia-%23000000.svg?style=for-the-badge&logo=wikipedia&logoColor=white)

## Install and Run Locally

- Python installation is required (contact if help needed)
- Clone the repository
- Navigate to the project directory `cd Detective-Discord`
- Create a virtual environment and activate it (optional)
- Install the required libraries `pip install -r requirements.txt`
- Create a `.env` file and add your discord bot TOKEN. Adding NEWS_API, WEATHER_API KEYS is optional. Remember to remove their commands if you wish to not include them.
- Run the bot using command `python3 bot.py`

## Steps to contribute:

- Drop a :star: on the Github repository (optional)<br/>
- Search for an issue on the repo which you can sort out and get assigned to it
- You can also make non-tech contributions by improving the readme or contribution guidelines files.
- Refer <a href="https://github.com/kanakmi/Detective-Discord/blob/Version-2.0/CONTRIBUTING.md">Contribution Guidelines</a> for a detailed contribution guide.

## Contributors

<a href="https://github.com/kanakmi/Detective-Discord/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=kanakmi/Detective-Discord&&max=817" />
</a>

## ❤️ Project Admin

| <a href="https://github.com/kanakmi"><img src="https://avatars.githubusercontent.com/u/54859521?v=4" width=150px height=150px /></a> |
| :----------------------------------------------------------------------------------------------------------------------------------: |
|                                           **[Kanak Mittal](https://twitter.com/Kanakmi)**                                            |
