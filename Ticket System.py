import discord
from discord import voice_client
from discord.embeds import Embed
from discord.ext import commands
import json
import asyncio
from discord_components import DiscordComponents, Button, Select, SelectOption, Component
from discord_components import *
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio
import io
from PIL import *
from PIL import Image, ImageFilter, ImageDraw
from datetime import *
import numpy as np
import random
import chat_exporter

intents = discord.Intents.default()
intents.members = True

Farben = [0x2f3136]


# json
async def save(path,ob):
    """await save("database/json/bot_config.json", setupdata)"""
    with open(path, "w") as f:
        json.dump(ob,f, indent = 4)



def load():
    with open("database/json/bot_config.json", "r") as file:
        return json.load(file)


data = load()

client = commands.Bot(command_prefix=data["prefix"], intents=intents)
client.remove_command("help")
client.launch_time = datetime.utcnow()


# app code


@client.event
async def on_ready():
    
    print('We have logged in as {0.user}'.format(client))
    DiscordComponents(client)

def _color_():
    return 0x2f3136

@client.command()
async def ticketsetup(ctx):
    with open("database/json/ticket-configs.json", "r") as f:
        setupdata = json.load(f)
    guild = ctx.guild
    color = _color_()

    if not ctx.guild.id in setupdata:
        setupdata[str(guild.id)] = {} #[guild.id]
        setupdata[str(guild.id)]["ticket-channel-id"] = 0
        setupdata[str(guild.id)]["ticket-title"] = "embed-title"
        setupdata[str(guild.id)]["embed-description"] = "embed-description"
        setupdata[str(guild.id)]["ticket-message-id"] = 0
        setupdata[str(guild.id)]["ticket-category-id"] = 0
        setupdata[str(guild.id)]["ticket_channel-ids"] = []  
        setupdata[str(guild.id)]["ticket-counter"] = 0

        await save("database/json/ticket-configs.json", setupdata)


    def mcheck(m):
        return m.author is not None and m.author == ctx.author



    embed = discord.Embed(title="Ticket System Setup", description="Please send the __Name__ the Ticket Embed should have", color=color)
    embed.set_footer(text=ctx.guild.name, icon_url=f"{ctx.guild.icon_url}")
    embed.timestamp = datetime.utcnow()
    msg1 = await ctx.send(embed=embed)
    msg = await client.wait_for('message', check=mcheck)
    setupdata[str(guild.id)]["ticket-title"] = f"{msg.content}"
    await msg1.add_reaction("✅")
    await save("database/json/ticket-configs.json", setupdata)

    embed = discord.Embed(title="Ticket System Setup", description="What should be the Text in the Ticket embed?", color=color)
    embed.set_footer(text=ctx.guild.name, icon_url=f"{ctx.guild.icon_url}")
    embed.timestamp = datetime.utcnow()
    msg1 = await ctx.send(embed=embed)
    msg = await client.wait_for('message', check=mcheck)
    setupdata[str(guild.id)]["ticket-description"] = f"{msg.content}"
    await msg1.add_reaction("✅")
    await save("database/json/ticket-configs.json", setupdata)

    embed = discord.Embed(title="Ticket System Setup", description="Please ping the channel where the Ticket message will get send in. #channel", color=color)
    embed.set_footer(text=ctx.guild.name, icon_url=f"{ctx.guild.icon_url}")
    embed.timestamp = datetime.utcnow()
    msg1 = await ctx.send(embed=embed)
    msg = await client.wait_for('message', check=mcheck)
    try:
        setupdata[str(guild.id)]["ticket-channel-id"] = msg.channel_mentions[0].id
        await msg1.add_reaction("✅")
        await save("database/json/ticket-configs.json", setupdata)
    except:
        await ctx.send("Channel not found please try again!")
        return


    embed = discord.Embed(title="Ticket System Setup", description="Please send the Category **ID** where the Ticket channels will get created.", color=color)
    embed.set_footer(text=ctx.guild.name, icon_url=f"{ctx.guild.icon_url}")
    embed.timestamp = datetime.utcnow()
    msg1 = await ctx.send(embed=embed)
    msg = await client.wait_for('message', check=mcheck)
    setupdata[str(guild.id)]["ticket-category-id"] = int(msg.content)
    await msg1.add_reaction("✅")
    await save("database/json/ticket-configs.json", setupdata)

    embed = discord.Embed(title="Ticket System Setup", description="Please edit the category as you want which roles have acces to the ticket! Only do this i will do the rest! (wait 10 seconds)\n\n\n💮Important: Unsync the Channel where the Ticket message will get send in!💮", color=color)
    embed.set_footer(text=ctx.guild.name, icon_url=f"{ctx.guild.icon_url}")
    embed.timestamp = datetime.utcnow()
    msg1 = await ctx.send(embed=embed)
    await msg1.add_reaction("✅")
    await asyncio.sleep(10)
    await save("database/json/ticket-configs.json", setupdata)
    channel = client.get_channel(setupdata[str(guild.id)]["ticket-channel-id"])
    embed = discord.Embed(title="Ticket System Setup", description=f"Sucessfully finished the Setup! I will send a message in {channel.mention}!", color=color)
    embed.set_footer(text=ctx.guild.name, icon_url=f"{ctx.guild.icon_url}")
    embed.timestamp = datetime.utcnow()
    msg1 = await ctx.send(embed=embed)
    await msg1.add_reaction("✅")
    embed = discord.Embed(title=setupdata[str(guild.id)]["ticket-title"], description=setupdata[str(guild.id)]["ticket-description"], color=color)
    embed.set_footer(text=ctx.guild.name, icon_url=f"{ctx.guild.icon_url}")
    
    ticket_msg = await channel.send(embed=embed)
    setupdata[str(guild.id)]["ticket-message-id"] = int(ticket_msg.id)
    await ticket_msg.add_reaction("🎟️")
    await save("database/json/ticket-configs.json", setupdata)




@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):



    color = 0x2f3136
    channel = client.get_channel(payload.channel_id)
    user =  client.get_user(payload.user_id)
    guild = client.get_guild(payload.guild_id)
    message = await channel.fetch_message(payload.message_id)
    with open("database/json/ticket-configs.json", "r") as file:
        setupdata = json.load(file)


    user = await client.fetch_user(payload.user_id)
    if (user.bot):
        return


    message_id = payload.message_id
#    if payload.channel_id == 
    if message_id == setupdata[str(guild.id)]["ticket-message-id"]:
        channel = client.get_channel(payload.channel_id)
        user =  client.get_user(payload.user_id)
        guild = client.get_guild(payload.guild_id)
        message = await channel.fetch_message(payload.message_id)

        if str(payload.emoji) == "🎟️":
            await message.remove_reaction("🎟️", user)
            
            color = 0x2f3136
            embed = discord.Embed(color=color)
            embed.set_author(name=f"Ticket for {user.name}", icon_url=user.avatar_url)
            embed.add_field(name="Ticket created!🎟️", value=f"Sucessfully created a ticket for: \n\n> `{user.name}` | {user.mention} | `{user.id}`\n\n\nPlease tell us your problem in this channel and we will try to help you as soon as possible")
            embed.set_thumbnail(url=guild.icon_url)
            embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon_url}")
            emb1 = Embed(title="Ticket is Creating...", description="", color=color)

            msg = await user.send(embed=emb1)
            category = client.get_channel(setupdata[str(guild.id)]["ticket-category-id"])
            cnt_ = setupdata[str(guild.id)]["ticket-counter"]
            ticket_channel = await category.create_text_channel(f"Ticket #{int(cnt_)}", topic=f"Ticket for {user.name}", permission_synced=True)
            await ticket_channel.set_permissions(user, read_message_history=True, read_messages=True, send_messages=True, add_reactions=True)
#            setupdata[str(guild.id)]["ticket_info"]["channel-id"] = int(ticket_channel.id))
#            setupdata[str(guild.id)]["ticket_info"]["user-id"] = int(user.id))
            setupdata[str(guild.id)]["ticket_channel-ids"].append(int(ticket_channel.id))
            setupdata[str(guild.id)][f"{ticket_channel.id} / {ticket_channel.name} / {guild.id}"] = {}
            setupdata[str(guild.id)][f"{ticket_channel.id} / {ticket_channel.name} / {guild.id}"]["user-id"] = user.id
            setupdata[str(guild.id)][f"{ticket_channel.id} / {ticket_channel.name} / {guild.id}"]["guild-name"] = str(guild.name)
            setupdata[str(guild.id)][f"{ticket_channel.id} / {ticket_channel.name} / {guild.id}"]["added-users-ids"] = []
            setupdata[str(guild.id)][f"{ticket_channel.id} / {ticket_channel.name} / {guild.id}"]["voice_channel-ids"] = []
            setupdata[str(guild.id)][f"{ticket_channel.id} / {ticket_channel.name} / {guild.id}"]["page_counter"] = 1
            setupdata[str(guild.id)]["ticket-counter"] += 1



            await save("database/json/ticket-configs.json", setupdata)
            msg_1 = await ticket_channel.send(embed=embed)
            await msg_1.add_reaction("⬅️")
            await msg_1.add_reaction("❌")
            await msg_1.add_reaction("🗒️")
            await msg_1.add_reaction("🔐")
            await msg_1.add_reaction("♻️")
            await msg_1.add_reaction("👤")
            await msg_1.add_reaction("🔈")
            await msg_1.add_reaction("➡️")
            emb2 = Embed(title="Ticket has got Created🎟️", description="> Ticket Channel: " + ticket_channel.mention, color=color)
            await asyncio.sleep(1)
            await msg.edit(embed=emb2)
            await msg.add_reaction("✅")





    if payload.channel_id in setupdata[str(guild.id)]["ticket_channel-ids"] and str(payload.emoji) == "❌":
        ticket_user = guild.get_member(setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["user-id"])
        await message.remove_reaction("❌", user)
        embed_1a = discord.Embed(color=color)
        embed_1a.add_field(name=f"{user.name} :x:", value=f"This channel got **deleted by {user.mention}** \n\n📌The Channel {channel.mention} will get deleted in **2** seconds!")
        embed_1a.set_footer(text=f"Ticket in {guild.name}", icon_url=f"{guild.icon_url}")
        await channel.send(embed=embed_1a)

        for id in setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["voice_channel-ids"]:
            channel_ = client.get_channel(id)
            try:
                await channel_.delete()
                emb = Embed(title=f"Channel Deleted🔈", description=f"Voice Channel got deleted:\n> `{channel_.name}` *#-#-#* `{id}`!", color=color)
                await channel.send(embed=emb)

            except commands.MissingPermissions:
                await channel.send("I have no Permissions to delete Channels please Fix this!")
                return

        transcript = await chat_exporter.export(channel, limit=9999, set_timezone="europe/berlin")
        await asyncio.sleep(2)
        

        if transcript is None:
             return

        transcript_file = discord.File(io.BytesIO(transcript.encode()),
                                                        filename=f"transcript-{channel.name}.html")
        emb = Embed(title=f"Ticket🎟️", description=f"Your Ticket in `{guild.name}` got closed by `{user.name}#{user.discriminator}`!\n\n\nI will send you a Transcript of the Ticket.🗒️\n\nYou have to download the File/Code and open it from your Browser or something else!", color=color)
        await ticket_user.send(embed=emb)
        await ticket_user.send(file=transcript_file)
        await channel.delete()


        

        index = setupdata[str(guild.id)]["ticket_channel-ids"].index(channel.id)
        del setupdata[str(guild.id)]["ticket_channel-ids"][index]
        del setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]
        await save("database/json/ticket-configs.json", setupdata)
        

    if payload.channel_id in setupdata[str(guild.id)]["ticket_channel-ids"] and str(payload.emoji) == "🗒️":
        await message.remove_reaction("🗒️", user)
        loading_embed = discord.Embed(color=color)
        loading_embed.set_author(name="Loading Chat, Users, Messages and Time!", icon_url="https://cdn.discordapp.com/emojis/806591946730504212.gif?v=1 ")
        msg = await channel.send(embed=loading_embed)
        tz_info = "europe/berlin"
        transcript = await chat_exporter.export(channel, limit=250, set_timezone="europe/berlin")

        if transcript is None:
             return

        transcript_file = discord.File(io.BytesIO(transcript.encode()),
                                                        filename=f"transcript-{channel.name}.html")

        await channel.send(file=transcript_file)
        await msg.delete()
        embed = Embed(title="Download the File/Code and open it.", description="", color=color)
        await channel.send(embed=embed)

    if payload.channel_id in setupdata[str(guild.id)]["ticket_channel-ids"] and str(payload.emoji) == "🔐":
        await message.remove_reaction("🔐", user)

        if setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["added-users-ids"]:
            emb = Embed(title="Unable to Lock🔐", description=f"Please remove the Users you added via the `👤` Reaction!", color=color)
            await channel.send(embed=emb)
            return

        ticket_user = guild.get_member(setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["user-id"])
        
        await channel.set_permissions(ticket_user, read_message_history=False, read_messages=False, send_messages=False, add_reactions=False)
        emb = Embed(title="Channel Locked🔐", description=f"{ticket_user.mention} **cannot send, read or react to a message** now, he can only read them!", color=color)
        await channel.send(embed=emb)
        await message.clear_reactions()
        await message.add_reaction("🔓")

        for id in setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["voice_channel-ids"]:
            channel_ = client.get_channel(id)
            await channel_.set_permissions(ticket_user, connect=False, view_channel=True)
            emb = Embed(title=f"🔈Channel Locked🔐", description=f"{ticket_user.mention} **cannot connect** to the channel:\n> `{channel_.name}` *#-#-#* `{id}`!", color=color)
            await channel.send(embed=emb)


    if payload.channel_id in setupdata[str(guild.id)]["ticket_channel-ids"] and str(payload.emoji) == "🔓":
        ticket_user = guild.get_member(setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["user-id"])
        await message.remove_reaction("🔓", user)
        await channel.set_permissions(ticket_user, read_message_history=True, read_messages=True, send_messages=True, add_reactions=True)
        emb = Embed(title="Channel unlocked🔓", description=f"{ticket_user.mention}  **can now send, read and react to a message** again!", color=color)
        await channel.send(embed=emb)
        for id in setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["voice_channel-ids"]:
            channel_ = client.get_channel(id)
            await channel_.set_permissions(ticket_user, connect=True, view_channel=True)
            emb = Embed(title=f"🔈Channel unlocked🔐", description=f"{ticket_user.mention} **can now connect** to the channel:\n> `{channel_.name}` *#-#-#* `{id}`!", color=color)
            await channel.send(embed=emb)
        await message.clear_reactions()
        await message.add_reaction("⬅️")
        await message.add_reaction("❌")
        await message.add_reaction("🗒️")
        await message.add_reaction("🔐")
        await message.add_reaction("♻️")
        await message.add_reaction("👤")
        await message.add_reaction("🔈")
        await message.add_reaction("➡️")
    

    if payload.channel_id in setupdata[str(guild.id)]["ticket_channel-ids"] and str(payload.emoji) == "♻️":
        ticket_user = guild.get_member(setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["user-id"])
        await channel.purge()
        embed = discord.Embed(color=color, title="Page 1/3📖")
        embed.set_author(name=f"Ticket for {user.name}", icon_url=user.avatar_url)
        embed.add_field(name="Ticket created!🎟️", value=f"Sucessfully created a ticket for: \n\n> `{ticket_user.name}` | {ticket_user.mention} | `{ticket_user.id}`\n\n\nPlease tell us your problem in this channel and we will try to help you as soon as possible")
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon_url}")   
        msg_1 = await channel.send(embed=embed)
        await msg_1.add_reaction("⬅️")
        await msg_1.add_reaction("❌")
        await msg_1.add_reaction("🗒️")
        await msg_1.add_reaction("🔐")
        await msg_1.add_reaction("♻️")
        await msg_1.add_reaction("👤")
        await msg_1.add_reaction("🔈")
        await msg_1.add_reaction("➡️")
        setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["page_counter"] = 1
        await save("database/json/ticket-configs.json", setupdata)
    
    if payload.channel_id in setupdata[str(guild.id)]["ticket_channel-ids"] and str(payload.emoji) == "👤":
        ticket_user = guild.get_member(setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["user-id"])
        await message.remove_reaction("👤", user)
        embed = Embed(title="Select your Option👤", description=f"Select if you want to `add` or `remove` a user from the Ticket.", color=color)
        msg2 = await channel.send(embed=embed,
        components = [Select(placeholder="Select the Command!", options=[
            SelectOption(
                label="add",
                value="add a user to the ticket channel!",
                description="add a user to the ticket channel.",
                emoji="➕"
            ),
            SelectOption(
                label="remove",
                value="remove a user from the ticket channel!",
                description="remove a user from the ticket channel.",
                emoji="➖"
            )
        ])])

        res = await client.wait_for("select_option")
        label = res.component[0].label

        if label == "add":
            await res.respond(type=6)
            emb = Embed(title="Add a Person👤", description="Please send me the **id** of the ticket_user i should add.", color=color)
            msg1 = await channel.send(embed=emb)
            def mcheck(m):
                return user is not None and user == user
            msg = await client.wait_for('message', check=mcheck)
            
            adding_user = guild.get_member(int(msg.content))
            await channel.set_permissions(adding_user, read_message_history=True, read_messages=True, send_messages=True, add_reactions=True)
            emb = Embed(title="Added a Person👤", description=f"I added `{adding_user.name}#{adding_user.discriminator}` to the Ticket `{channel.name}`!", color=color)
            await msg.delete()
            await msg1.delete()
            await msg2.delete()
            await channel.send(embed=emb)
            emb  = Embed(title="You got added👤🎟️!", description=f"`{user.name}#{user.discriminator}` added you to the Ticket {channel.mention}!", color=color)
            await adding_user.send(embed=emb)
            setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["added-users-ids"].append(int(adding_user.id))
            await save("database/json/ticket-configs.json", setupdata)

        if label == "remove":
            
            if not setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["added-users-ids"]:
                await res.respond(type=6)
                embed = Embed(title="There are no more Users you can remove from the Ticket", color=color)
                return

            await res.respond(type=6)
            emb = Embed(title="Remove a Person👤", description="Please send me the **id** of the ticket_user i should remove.", color=color)
            msg1 = await channel.send(embed=emb)
            def mcheck(m):
                return user is not None and user == user
            msg = await client.wait_for('message', check=mcheck)
            removing_user = guild.get_member(int(msg.content))
            await channel.set_permissions(removing_user, read_message_history=False, read_messages=False, send_messages=False, add_reactions=False)
            emb = Embed(title="Removed a Person👤", description=f"I removed `{removing_user.name}#{removing_user.discriminator}` from to the Ticket `{channel.name}`!", color=color)
            await msg.delete()
            await msg1.delete()
            await msg2.delete()
            await channel.send(embed=emb)
            emb  = Embed(title="You got removed👤🎟️!", description=f"`{user.name}#{user.discriminator}` removed you from to the Ticket {channel.mention}!", color=color)
            await removing_user.send(embed=emb)
            index = setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["added-users-ids"].index(int(removing_user.id))
            del setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["added-users-ids"][index]
            await save("database/json/ticket-configs.json", setupdata)

    if payload.channel_id in setupdata[str(guild.id)]["ticket_channel-ids"] and str(payload.emoji) == "🔈":
        ticket_user = guild.get_member(setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["user-id"])
        await message.remove_reaction("🔈", user)
        color = 0x2f3136


        category = client.get_channel(setupdata[str(guild.id)]["ticket-category-id"])
        voice_channel = await category.create_voice_channel(f"Voice: {ticket_user.name} 🔈", topic=f"Ticket for {ticket_user.name}", permission_synced=True)
        await voice_channel.set_permissions(ticket_user, read_message_history=True, read_messages=True, send_messages=True, add_reactions=True)

        embed = discord.Embed(color=color)
        embed.set_author(name=f"Voice Channel for {ticket_user.name}", icon_url=user.avatar_url)
        embed.add_field(name="Channel created!🔈", value=f"Sucessfully created a Voice Channel for: \n\n> `{ticket_user.name}` | {ticket_user.mention} | `{ticket_user.id}`\n\n\nInfos:\n       {voice_channel.name} | {voice_channel.id} ")
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon_url}")
        await channel.send(embed=embed)
        setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["voice_channel-ids"].append(int(voice_channel.id)) 

        await save("database/json/ticket-configs.json", setupdata)

    if payload.channel_id in setupdata[str(guild.id)]["ticket_channel-ids"] and str(payload.emoji) == "⬅️":
        ticket_user = guild.get_member(setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["user-id"])
        await message.remove_reaction("⬅️", user)
        color = 0x2f3136

        if setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["page_counter"] == 1:
            return
            
        
        if setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["page_counter"] == 2:
            embed = discord.Embed(color=color, title="Page 1/3📖")
            embed.set_author(name=f"Ticket for {user.name}", icon_url=user.avatar_url)
            embed.add_field(name="Ticket created!🎟️", value=f"Sucessfully created a ticket for: \n\n> `{user.name}` | {user.mention} | `{user.id}`\n\n\nPlease tell us your problem in this channel and we will try to help you as soon as possible")
            embed.set_thumbnail(url=guild.icon_url)
            embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon_url}")
            try:
                await message.edit(embed=embed)
                setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["page_counter"] = 1
            except:
                return print("error")
            await save("database/json/ticket-configs.json", setupdata)

        if setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["page_counter"] == 3:
            embed = discord.Embed(color=color, title="Page 2/3📖")
            embed.set_author(name=f"Voice Channel for {ticket_user.name}", icon_url=user.avatar_url)
            embed.add_field(name="❌", value=f"Deletes The Ticket\n ", inline=False)
            embed.add_field(name="🗒️", value=f"Send a Transcript of the Ticket channel\n ", inline=False)
            embed.add_field(name="🔐", value=f"locks the channel so the ticket creator cant write, read and other stuff. Also Voicechannel\n ", inline=False)
            embed.add_field(name="🔓", value=f"unlocks the channel. Also Voicechannel\n ", inline=False)
            embed.add_field(name="♻️", value=f"Clears the Channel history (delete all messages)\n ", inline=False)
            embed.add_field(name="👤", value=f"You can add a ticket_user to the channel or remove a ticket_user from the channel\n ", inline=False)
            embed.add_field(name="🔈", value=f"Creates a Voice Channel so you can talk to the Ticket Creator\n ", inline=False)
            embed.set_thumbnail(url=guild.icon_url)
            embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon_url}")
            try:
                await message.edit(embed=embed)
                setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["page_counter"] = 2
            except:
                return print("error")

            await save("database/json/ticket-configs.json", setupdata)





    if payload.channel_id in setupdata[str(guild.id)]["ticket_channel-ids"] and str(payload.emoji) == "➡️":
        ticket_user = guild.get_member(setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["user-id"])
        await message.remove_reaction("➡️", user)
        color = 0x2f3136

        if setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["page_counter"] == 2:
            await save("database/json/ticket-configs.json", setupdata)
            
        if setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["page_counter"] == 2:
            roles = []
            for role in ticket_user.roles:
                roles.append(role)

            embed = discord.Embed(title='Page 3/3📖 | 👤 Userinfo 👤',
                                color=color,
                                description=f'User: {ticket_user.mention}',
                                timestamp=message.created_at)
            embed.add_field(name='__**Bot:**__',
                            value=f'{("Ja" if ticket_user.bot else "Nein")}',
                            inline=False)
            embed.add_field(name="__**ID:**__", value=f'{ticket_user.id}', inline=False)
            embed.add_field(
                name='__**Nickname:**__',
                value=f'{(ticket_user.nick if ticket_user.nick else "Nicht gesetzt")}',
                inline=False)
            embed.add_field(name=f'**__{message.guild}__** beigetreten:',
                            value=ticket_user.joined_at.strftime('%d/%m/%Y, %H:%M:%S'),
                            inline=False)
            embed.add_field(name='**__Discord__** beigetreten:',
                            value=ticket_user.created_at.strftime('%d/%m/%Y, %H:%M:%S'),
                            inline=False)
            embed.add_field(name='__**Booster:**__',
                            value=f'{("Ja" if ticket_user.premium_since else "Nein")}',
                            inline=False)
            embed.add_field(name='__**Farbe:**__', value=f'{ticket_user.color}', inline=True)
            embed.add_field(name='**__Höchste Rolle:__**',
                            value=f'<@&{ticket_user.top_role.id}>',
                            inline=False)

            embed.add_field(name=f"**__Rollen:__** ({len(roles)})",
                            value=" ".join([role.mention for role in roles]))       
            embed.set_thumbnail(url=user.avatar_url)
            embed.set_footer(text=f'Angefordert von {user} • {user.id}',
                            icon_url=user.avatar_url)
            try:
                await message.edit(embed=embed)
                setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["page_counter"] = 3
            except:
                return print("error")
            
            await save("database/json/ticket-configs.json", setupdata)        


        if setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["page_counter"] == 1:
            embed = discord.Embed(color=color, title="Page 2/3📖")
            embed.set_author(name=f"Voice Channel for {ticket_user.name}", icon_url=user.avatar_url)
            embed.add_field(name="❌", value=f"Deletes The Ticket\n ", inline=False)
            embed.add_field(name="🗒️", value=f"Send a Transcript of the Ticket channel\n ", inline=False)
            embed.add_field(name="🔐", value=f"locks the channel so the ticket creator cant write, read and other stuff. Also Voicechannel\n ", inline=False)
            embed.add_field(name="🔓", value=f"unlocks the channel. Also Voicechannel\n ", inline=False)
            embed.add_field(name="♻️", value=f"Clears the Channel history (delete all messages)\n ", inline=False)
            embed.add_field(name="👤", value=f"You can add a ticket_user to the channel or remove a ticket_user from the channel\n ", inline=False)
            embed.add_field(name="🔈", value=f"Creates a Voice Channel so you can talk to the Ticket Creator\n ", inline=False)
            embed.add_field(name="🤖", value=f"Bot Dev: *Svaxyy | Lenny#0859*  ", inline=False) # Note to me bcs you can use the code for free so support me
            embed.set_thumbnail(url=guild.icon_url)
            embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon_url}")
            try:
                await message.edit(embed=embed)
                setupdata[str(guild.id)][f"{channel.id} / {channel.name} / {guild.id}"]["page_counter"] = 2
            except:
                return print("error")
            await save("database/json/ticket-configs.json", setupdata)
            














        

        






            
        



client.run(data["token"])
