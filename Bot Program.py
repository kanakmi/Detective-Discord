import discord
import re

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

TOKEN = 'YOUR TOKEN HERE'

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

        if(domain == "discord.gift" or domain == "discord.gg"):
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
            await message.channel.send("{} has been warned for nitro scamming. They are now {} steps closer from getting banned.".format(message.author.mention, 3-warnings))
        else:
            await message.channel.send("{} has been banned for nitro scamming.".format(message.author.mention))
            await message.author.send("You have been banned for nitro scamming. Please contact a staff member if you believe this is a mistake.")
            await message.author.ban()


client.run(TOKEN)