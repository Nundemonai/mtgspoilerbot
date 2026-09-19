"""
Configuration file for the Discord bot.

To create this bot, go to https://discord.com/developers/applications
Login and start creating your bot.

IMPORTANT:
1. Save settings if they ask you to.
2. In the General Information tab, give your bot a name and description, and get your CLIENT_ID variable (Application ID).
3. Save and continue onwards to Installation.
4. Use User Install and Guild Install in the Installation Context.
5. Go to the link provided. Register it to the server you want it installed onto.
6. Go to the Bot tab and give it a username and profile picture/banner if desired.
7. Press "Reset Token" and put it in the CLIENT_SECRET variable (Don't share this with anyone, not even your grandma!)
8. Enable "Public Bot", "Presence Intent", and "Message Content Intent".
9. In the Bot Permissions tab, give it "Send Messages", "Create Public Threads", and "Create Private Threads".
10. You should now be good to go!

HOW TO USE:
Create a forum channel in your Discord server:
1. Create a new text channel and make it into a Forum one.
2. Once created, right-click the channel and choose "Copy Channel ID" (At this stage, automatic creation hasn't been implemented yet.)

Go to MythicSpoilers website and choose a set. Let's say the Star Trek set. Their link looks like this:
https://mythicspoiler.com/trk/index.html

All you want from this link is the "trk" part.
Write the command as "!setnames trk" and a new text channel should be created with the name of "trk" and will 
spit out the spoiled cards in order.

"""

# Configuration Settings

# Replace 'channel_id' with the actual Channel ID of your Forum in Discord
FORUM_ID = "channel_id"

# Command prefix used to activate the bot. Change if you want another prefix, e.g., "!set"
COMMAND_PREFIX = "!setnames"

# Optional: Specify a specific channel where the command can be used.
# If left empty or None, the command will work in all channels where the bot is added.
SPECIFIC_CHANNEL = "general"  # Change this to a specific channel you want to use the command from.

# Replace 'Allowed_role' with the role name that members need to have to use the command
ELIGIBILITY_ROLE = 'Allowed_role'

# Bot Credentials
CLIENT_ID = 'client_id'      # Your bot's ID (Application ID)
CLIENT_SECRET = 'client_secret'  # Your bot's secret token. Keep this secure!
DISCORD_BOT_TOKEN = 'bot_token'  # Your bot's authentication token. Also keep this secure!

# Server Information
SERVER_ID = 'server_id'  # The ID of the server where the bot will be used

# End of Configuration
