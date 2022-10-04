import discord
from discord import Option
from discord.ext import commands
from discord.ext.commands import MissingPermissions
import re
import requests
import sqlite3
import wikipedia
import pyjokes

TOKEN = "PUT YOUR DISCORD BOT TOKEN HERE"
NEWS_API = "PUT YOUR API KEY HERE"
WEATHER_API = "PUT YOUR API KEY HERE"

class warning:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')

        c = self.conn.cursor()

        try:
            c.execute("""
                        CREATE TABLE warnings (
                            id text PRIMARY KEY,
                            warnings int
                        )
                    """)
            self.conn.commit()

        except:
            print("Table already exists")

        c.close()

    def insertWarning(self, id):
        c = self.conn.cursor()
        try:
            c.execute("INSERT INTO warnings VALUES (?, 1)", (id,))
            self.conn.commit()
            c.close()
            return 1
        except:
            c.execute("UPDATE warnings SET warnings = warnings + 1 WHERE id = ?", (id,))
            c.execute("SELECT warnings FROM warnings WHERE id = ?", (id,))
            warnings = c.fetchone()[0]
            self.conn.commit()
            c.close()
            return warnings
    
    def deleteWarning(self, id):
        try:
            c = self.conn.cursor()
            c.execute("DELETE FROM warnings WHERE id = ?", (id,))
            self.conn.commit()
            c.close()
            return True
        except:
            return False

data_obj = warning()

class NitroScam:
    def __init__(self):
        self.safe_domains = ["discord.gift", "discord.com", "discord.gg", "discord.me", "discord.io", "discordapp.com"]
    
    # function to check if the string contains a url and return the url
    def __contains_url__(self, message):
        return re.findall(r'(https?://\S+)', message)
    
    # Levenstien Distance
    # function to check the number of insertions/deletions have to be done to make two strings identical
    # lesser the number, more similar the strings are
    def __similarity__(self, domain):
        string2 = "discord"
        m = len(domain)
        n = 7
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n+1):
                if domain[i-1] == string2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        return (m+n)-(2*dp[m][n])
    
    def checkNitroScam(self, message):
        url = self.__contains_url__(message)

        # check if the string contains a url
        if(len(url) == 0):
            return 0
        
        splitted = url[0].split("/")
        domain = splitted[2]

        # domain is safe
        if domain in self.safe_domains:
            return 0

        domainName = domain.split(".")[0]

        if(len(domainName)>6):
            sim = self.__similarity__(domainName[:7])
        else:
            sim = self.__similarity__(domainName)

        if sim < 5:
            return 1
        else:
            # if message contains a url and words discord and nitro, then it could be a scam
            message = message.split()
            if "discord" in message and "nitro" in message:
                return 2
    
    def addSafeDomain(self, domain):
        if domain not in self.safe_domains:
            self.safe_domains.append(domain)
    
    def deleteSafeDomain(self, domain):
        if domain in self.safe_domains:    
            self.safe_domains.remove(domain)

nitroscam_obj = NitroScam()

def NewsFromBBC(): 
    main_url = "https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=" + NEWS_API
    open_bbc_page = requests.get(main_url).json() 
    article = open_bbc_page["articles"] 
    results = [] 
    for ar in article: 
        results.append(ar["title"])
        results.append("Read more - " + ar["url"])
        if len(results) == 10:
            break
    return "\n".join(results)

def weatherDetails(city):
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + WEATHER_API
    x = requests.get(url).json()
    y = x["main"]
    current_temperature = y["temp"]-273 
    current_temperature = round(current_temperature, 2)
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

def runMessageCommands():
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        msg = message.content.lower()

        x = nitroscam_obj.checkNitroScam(msg)
        if x==1:
            try:
                await message.delete()
                warnings = data_obj.insertWarning(str(message.author))
                if warnings < 3:
                    await message.channel.send("{} has been warned for nitro scamming. They are now {} warnings away from getting kicked.".format(message.author.mention, 3-warnings))
                else:
                    await message.channel.send("{} has been kicked for nitro scamming.".format(message.author.mention))
                    await message.author.send("You have been kicked for nitro scamming. Please contact a staff member if you believe this is a mistake.")
                    await message.author.kick()
                    data_obj.deleteWarning(str(message.author))
            except:
                x=2

        if x==2:
            await message.reply("This seems like a nitro scam link. Please be cautious while opening it. Please contact a staff member if you believe this is a mistake.")

    client.run(TOKEN)

def runSlashCommands():
    bot = discord.Bot()

    @bot.event 
    async def on_ready():
        print(f"We've logged in as {bot.user}.")

    # testing = [934343872232976384] #list of guild ids

    @bot.slash_command(name = "wiki", description='Returns a Wikipedia summary')
    async def wiki(ctx, searchkey: Option(str, description="What do you want to search on wikipedia?", required = True)):
        try:
            result = wikipedia.summary(searchkey, sentences=2)
            try:
                await ctx.respond(result)
            except:
                await ctx.send(result)
        except:
            await ctx.respond('Sorry! Search Key not found.')

    @bot.slash_command(name = "joke", description='Returns a random joke')
    async def joke(ctx):
        joke = pyjokes.get_joke()
        await ctx.respond(joke)

    @bot.slash_command(name = "news", description='Returns the top 5 news from BBC')
    async def news(ctx):
        news = NewsFromBBC()
        await ctx.respond(news)

    @bot.slash_command(name = "weather", description='Returns the weather of a city')
    async def weather(ctx, city: Option(str, description="Enter the name of the city", required = True)):
        weather = weatherDetails(city)
        await ctx.respond(weather)

    @bot.slash_command(name="reset_warn", description="Reset warnings for a member")
    @commands.has_permissions(ban_members = True)
    async def reset_warn(ctx, member: Option(discord.Member, description="Member to reset warnings for", required = True)):
        res = data_obj.deleteWarning(str(member))
        if res:
            await ctx.respond("Warnings for {} have been reset.".format(member.mention))
        else:
            await ctx.respond("No warnings for {}.".format(member.mention))
    
    @reset_warn.error
    async def resetWarnError(ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond("You need Kick Members permissions to do this!")
        else:
            await ctx.respond("Something went wrong...")

    @bot.slash_command(name="safe_domain", description="Add a domain to the safe domains list")
    @commands.has_permissions(ban_members = True)
    async def safe_domain(ctx, domain: Option(str, description="Domain to add to the safe domains list", required = True)):
        nitroscam_obj.addSafeDomain(domain)
        await ctx.respond("{} has been added to the safe domains list.".format(domain))
    
    @safe_domain.error
    async def safeDomainError(ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond("You need Kick Members permissions to do this!")
        else:
            await ctx.respond("Something went wrong...")

    @bot.slash_command(name="unsafe_domain", description="Remove a domain from the safe domains list")
    @commands.has_permissions(ban_members = True)
    async def unsafe_domain(ctx, domain: Option(str, description="Domain to remove from the safe domains list", required = True)):
        nitroscam_obj.removeSafeDomain(domain)
        await ctx.respond("{} has been removed from the safe domains list.".format(domain))
    
    @unsafe_domain.error
    async def unsafeDomainError(ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond("You need Kick Members permissions to do this!")
        else:
            await ctx.respond("Something went wrong...")

    bot.run(TOKEN)


import multiprocessing

if __name__ == "__main__":
    process1 = multiprocessing.Process(target=runMessageCommands)
    process2 = multiprocessing.Process(target=runSlashCommands)

    process1.start()
    process2.start()
