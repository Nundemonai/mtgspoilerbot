from config import ELIGIBILITY, COMMAND, TOKEN, SPECIFIC_CHANNEL, FORUM_ID
import discord
from discord.ext import commands
import asyncio
import os
import logging
from imageReciever import get_cards

intents = discord.Intents.default()

intents.message_content = True
# bot = commands.Bot(command_prefix='!', intents=intents)
client = discord.Client(intents=intents)
logging.basicConfig(
    level=logging.DEBUG,
    filename='logs.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):

    if message.author == client.user:
        return
    mes_channels = message.channel.name

    if message.content.startswith(f"{COMMAND}"):
        if mes_channels == SPECIFIC_CHANNEL:
    
        
            roles = message.author.roles
            role_names = [role.name for role in roles]
            if ELIGIBILITY in role_names:
                await card_collector(message)
        else:
            await message.channel.send(f"You can only use this command in {SPECIFIC_CHANNEL} channel.")
    else:
        await message.channel.send("You don't have the permission to use this command.")

@client.event
async def on_raw_thread_delete(payload):
    file_name = f"sent_{payload.thread.name}.txt"
    if os.path.exists(file_name):
        try:
            os.remove(file_name)
            logging.info(f"File: {file_name} was removed.")
        except Exception as e:
            logging.error(f"File coud not be removed: {e}")
    

async def card_collector(message):
    try:
        forum_id = FORUM_ID
        set_name = message.content.split()[1]
        open(f"sent_{set_name}.txt", "a").close()
        await asyncio.sleep(0.1)
        forums = await client.fetch_channel(forum_id)
        all_threads = []
        for threaded in forums.threads:
            if threaded.name.lower() == set_name.lower():
                all_threads.append(threaded)
        def get_last_processed_letter():
            with open(f'sent_{set_name}.txt', 'r') as file:
                lines = file.readlines()
                if lines:
                    return lines[-1].strip()
                else:
                    return None
        card_urls = await get_cards(set_name)
        if not card_urls:
            await message.channel.send(f"No cards found for the set: {set_name}")
            return
        # Save all cards to a file
        with open (f"all_{set_name}.txt", "w") as f_all:
            f_all.write('\n'.join(card_urls))
            
        last_processed_link = get_last_processed_letter()
        if last_processed_link == None:
            start_index = 0
        else:
            with open(f"all_{set_name}.txt", "r") as read_file:
                lines = read_file.readlines()
                try:
                    start_index = lines.index(last_processed_link + "\n")
                except ValueError:
                    start_index = len(lines)
        if not all_threads:
            await message.channel.send(f"Creating new thread for set: {set_name}, the set has {len(card_urls)} cards in it.")
            try:
                logging.info(f"Creating a new thread for set '{set_name}'.")
                thread = await forums.create_thread(name=set_name, content=f"Here we spoil the latest cards from the newest set! {set_name}")
                logging.debug(f"Created new thread ID: {threaded.id}")
                # Send all new cards to the newly created thread
                with open(f'sent_{set_name}.txt', 'a') as sent:
                    for url in card_urls[start_index:]:
                        if not url.strip():
                            continue
                        await asyncio.sleep(0.5)  # Avoid hitting rate limits
                        await thread.message.channel.send(url)
                        sent.write(url + '\n')
            except Exception as e:
                logging.error(f"Failed to create or send cards to new thread for set '{set_name}': {e}", exc_info=True)
                await message.channel.send(f"Failed to create or send cards to new thread for set '{set_name}': {e}")
        else:
            
            # For each thread, send the remaining cards
            for threaded in all_threads:
                logging.info(f"Continuing in existing thread ID: {threaded.id} (Name: {threaded.name})")
                
                if not card_urls[start_index:]:
                    continue


                
            try:
                with open(f'all_{set_name}.txt', 'r') as all_card:
                    content_all = all_card.readlines()
                with open(f'sent_{set_name}.txt', 'r') as sent_card:
                    content_sent = sent_card.readlines()

                with open(f'sent_{set_name}.txt', 'a') as sent:
                    if len(content_sent) <= len(content_all):
                        await message.channel.send(f"Continuing in the existing thread for set: {set_name}")
                    else:
                        await message.channel.send(f"No more cards found for the set {set_name} at this point.")
                    # Send cards to the current thread
                    for url in card_urls[start_index:]:
                        if not url.strip():
                            continue
                        await asyncio.sleep(0.5)  # Avoid hitting rate limits
                        await threaded.send(url)
                        sent.write(url + '\n')
                
            except Exception as e:
                logging.error(f"Failed to send cards to existing thread ID {threaded.id} (Name: {threaded.name}): {e}", exc_info=True)
                    
    except Exception as e:
        await message.channel.send(f"An error occurred while fetching cards: {e}")
        logging.error(f"An error occurred while fetching cards: {e}")

client.run(TOKEN)