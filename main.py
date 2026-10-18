import os
import discord
from discord.ext import commands
import google.generativeai as genai

# 1. Configure the Gemini AI
genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. Configure the Discord Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - Online and Ready!')

# 3. Listen for @mentions or !ai commands
@bot.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == bot.user:
        return

    # Check if the bot was tagged or if the message starts with !ai
    if bot.user.mentioned_in(message) or message.content.startswith('!ai'):
        # Clean up the prompt text
        prompt = message.content.replace(f'<@{bot.user.id}>', '').replace('!ai', '').strip()
        
        if not prompt:
            await message.reply("Hi! Ask me anything.")
            return

        async with message.channel.typing():
            try:
                # Generate a response from Gemini
                response = model.generate_content(prompt)
                await message.reply(response.text)
            except Exception as e:
                await message.reply("Sorry, I ran into an error thinking about that.")
                print(e)

    await bot.process_commands(message)

# 4. Start the Bot using your secret token
bot.run(os.environ['DISCORD_TOKEN'])
