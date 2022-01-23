import discord
import re
import requests
import wikipedia as wiki
import pyjokes

TOKEN = "PUT YOUR DISCORD BOT TOKEN HERE"
NEWS_API = "PUT YOUR API KEY HERE"
WEATHER_API = "PUT YOUR API KEY HERE"

# Operations with the database
import sqlite3

conn = sqlite3.connect('users.db')

c = conn.cursor()

try:
    c.execute("""CREATE TABLE warnings (
                    id text PRIMARY KEY,
                    warnings int
    )""")
    conn.commit()

except:
    print("Table already exists")

def insert_warning(id):
    try:
        c.execute("INSERT INTO warnings VALUES (?, 1)", (id,))
        conn.commit()
        return 1
    except:
        c.execute("UPDATE warnings SET warnings = warnings + 1 WHERE id = ?", (id,))
        c.execute("SELECT warnings FROM warnings WHERE id = ?", (id,))
        warnings = c.fetchone()[0]
        conn.commit()
        return warnings

def delete_warning(id):
    try:
        c.execute("DELETE FROM warnings WHERE id = ?", (id,))
        conn.commit()
        return True
    except:
        return False

# instantiate the bot    
client = discord.Client()

# function to check if the string contains a url and return the url
def contains_url(string):
    return re.findall(r'(https?://\S+)', string)

# Levenstien Distance
# function to check the number of insertions/deletions have to be done to make two strings identical
# lesser the number, more similar the strings are
def similarity(string1):
    string2 = "discord"
    m = len(string1)
    n = 7
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n+1):
            if string1[i-1] == string2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return (m+n)-(2*dp[m][n])

def checkNitroScam(string):
    url = contains_url(string)

    # check if the string contains a url
    if(len(url) > 0):
        splitted = url[0].split("/")
        domain = splitted[2]

        if(domain == "discord.gift" or domain == "discord.gg" or domain == "discord.me" or domain == "discord.io" or domain == "discordapp.com/invite"):
            return False

        domainName = domain.split(".")[0]

        if(len(domainName)>6):
            sim = similarity(domainName[:7])
        else:
            sim = similarity(domainName)

        if sim < 4:
            return True
        else:
            trigger_words = ["nitro", "discord"]
            if any(word in string for word in trigger_words):
                return True
            else:
                return False
    else:
        return False

def NewsFromBBC(): 
    main_url = "https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=" + NEWS_API
    open_bbc_page = requests.get(main_url).json() 
    article = open_bbc_page["articles"] 
    results = [] 
    for ar in article: 
        results.append(ar["title"])
        results.append("Read more - " + ar["url"])
    return results[:10]

def weatherDetails(city):
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + WEATHER_API
    x = requests.get(url).json()
    y = x["main"]
    current_temperature = y["temp"]-273 
    current_temperature = round(current_temperature, 2)
    current_pressure = y["pressure"]
    current_humidiy = y["humidity"]
    z = x["weather"]
    weather_description = z[0]["description"] 
    return ("Weather in " + city.title() + 
          "\nTemperature = " +
                    str(current_temperature) + ' degree Celcius' +
          "\nHumidity = " +
                    str(current_humidiy) + '%' +
          "\nDescription = " +
                    str(weather_description)) 

@client.event
async def on_ready():
    print('Logged in as ' + str(client.user))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    string = message.content
    
    if checkNitroScam(string):
        await message.delete()
        warnings = insert_warning(str(message.author))
        if warnings < 3:
            await message.channel.send("{} has been warned for nitro scamming. They are now {} warnings away from getting banned.".format(message.author.mention, 3-warnings))
        else:
            await message.channel.send("{} has been banned for nitro scamming.".format(message.author.mention))
            await message.author.send("You have been banned for nitro scamming. Please contact a staff member if you believe this is a mistake.")
            await message.author.ban()
            delete_warning(str(message.author))

    elif string.startswith('$reset_warn'):
        roles = [role.name for role in message.author.roles]
        print(roles)
        if 'admin' not in roles and 'moderator' not in roles:
            await message.channel.send("You do not have permission to use this command.")
        else:
            user = string.split()[1][3:-1]
            user = await client.fetch_user(user)
            res = delete_warning(str(user))
            if res:
                await message.channel.send("{} warnings have been reset.".format(user.mention))
            else:
                await message.channel.send("{} doesn't have any warnings.".format(user.mention))
    
    elif string.startswith('$news'):
        await message.channel.send('News from BBC:')
        news = NewsFromBBC()
        for i in news:
            await message.channel.send(i)

    elif string.startswith('$weather'):
        city = string[9:]
        city = city.lower()
        try:
            weather = weatherDetails(city)
            await message.channel.send(weather)
        except:
            await message.reply('City not found')

    elif string.startswith('$joke'):
        joke = pyjokes.get_joke()
        await message.channel.send(joke)

    elif string.startswith('$wiki'):
        query = string[6:]
        try:
            result = wiki.summary(query, sentences=2)
            await message.reply(result)
        except:
            await message.reply('Sorry! Search Key not found.')

    elif string.startswith('$help'):
        await message.channel.send("""
        Commands:
        $news - Get latest news from BBC
        $weather <city> - Get weather in a city
        $joke - Get a random joke
        $wiki <search key> - Get a summary of a search key from Wikipedia
        $help - Get this message
        $reset_warn <user> - Reset warnings for a user (admin/moderator only)
        """)

    elif string.startswith('$'):
        await message.channel.send('Invalid command!')

client.run(TOKEN)
