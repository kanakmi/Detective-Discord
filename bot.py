import discord
from discord import Option
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from discord.ui import Button, View
import requests
from warning_class import Warning
from nitroscam_class import NitroScam
import wikipedia
import pyjokes
from dotenv import load_dotenv
import os
load_dotenv()

TOKEN = os.getenv("TOKEN")
NEWS_API = os.getenv("NEWS_API")
WEATHER_API = os.getenv("WEATHER_API")

data_obj = Warning()

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
    return ("Temperature = " +
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

    @bot.slash_command(name = "wiki", description='Returns a Wikipedia summary')
    async def wiki(ctx, searchkey: Option(str, description="What do you want to search on wikipedia?", required = True)):
        try:
            result = wikipedia.summary(searchkey, sentences=2)
            embed = discord.Embed(title=searchkey, description=result, color=0x00ff00)
            await ctx.respond(embed=embed)
        except:
            await ctx.respond('Sorry! Search Key not found.')

    @bot.slash_command(name = "joke", description='Returns a random joke')
    async def joke(ctx):
        joke = pyjokes.get_joke()
        await ctx.respond(joke)

    @bot.slash_command(name = "avatar", description='Returns mentioned user\'s avatar')
    async def avatar(ctx, avamember: Option(discord.Member, description="The member whose avatar you want to see.", required = False)):
        try:
            if avamember == None:
                userAvatarUrl = ctx.author.avatar.url
                name = ctx.author.name
                
            else:
                userAvatarUrl = avamember.avatar.url
                name = avamember.name
            embed = discord.Embed(title=('{}\'s Avatar'.format(name)),colour=discord.Colour.green())
            embed.set_image(url='{}'.format(userAvatarUrl))
            await ctx.respond(embed=embed)
        except:
            embed = discord.Embed(description='User has no Avatar ❌',color=discord.Color.red())
            await ctx.respond(embed=embed)

    @bot.slash_command(name = "news", description='Returns the top 5 news from BBC')
    async def news(ctx):
        news = NewsFromBBC()
        embed = discord.Embed(title="Top News from BBC", description=news, color=0x00ff00)
        await ctx.respond(embed=embed)

    @bot.slash_command(name = "weather", description='Returns the weather of a city')
    async def weather(ctx, city: Option(str, description="Enter the name of the city", required = True)):
        weather = weatherDetails(city)
        embed = discord.Embed(title=f"Weather in {city.title()}", description=weather, color=0x00ff00)
        await ctx.respond(embed = embed)

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

    @bot.slash_command(name="help", description="Know more about the commands of bot")
    async def help(ctx):
        github = Button(label='Star on Github', style=discord.ButtonStyle.success, url='https://github.com/kanakmi/Detective-Discord', emoji='⭐')
        twitter = Button(label='Follow on Twitter', style=discord.ButtonStyle.blurple, url='https://twitter.com/kanakmi', emoji='🐦')
        embed = discord.Embed(title="Detective Discord", description="Detective Discord is a bot that helps you detect nitro scams and other malicious links. It also has some other useful commands.", color=0x00ff00)
        response = "`/wiki` - Returns a Wikipedia summary" + '\n' + \
                    "`/joke` - Returns a random joke" + '\n' + \
                    "`/avatar` - Returns mentioned user's Avatar" + '\n' + \
                    "`/news` - Returns the top 5 news from BBC" + '\n' + \
                    "`/weather` - Returns the weather of a city" + '\n' + \
                    "`/reset_warn` - Reset warnings for a member (Admin/Mod only)" + '\n' + \
                    "`/safe_domain` - Add a domain to the safe domains list (Admin/Mod only)" + '\n' + \
                    "`/unsafe_domain` - Remove a domain from the safe domains list (Admin/Mod only)" + '\n' + \
                    "`/help` - Get this message"
        embed.add_field(name="Commands", value=response, inline=False)
        view = View()
        view.add_item(github)
        view.add_item(twitter)
        await ctx.respond(embed=embed, view=view)

    bot.run(TOKEN)

import multiprocessing

if __name__ == "__main__":
    process1 = multiprocessing.Process(target=runMessageCommands)
    process2 = multiprocessing.Process(target=runSlashCommands)

    process1.start()
    process2.start()
