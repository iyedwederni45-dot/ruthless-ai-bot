import discord
import os
import requests

# ===== ENV VARIABLES =====
TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# ===== DISCORD SETUP =====
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# ===== SERVER KNOWLEDGE (RUTHLESS) =====
SERVER_CONTEXT = """
You are the official AI assistant for the Discord server: RUTHLESS.

RUTHLESS is a competitive battlefield server where:
- Every member starts from zero
- Points are earned, not given
- Every 2 weeks a new season starts
- Only top players reach the leaderboard

RULES:
- Respect others (trash talk allowed, no personal attacks)
- No cheating or fake proof
- No spam, ads, politics, religion, or NSFW
- Stay on topic in channels
- Admin decisions are final

HOW IT WORKS:
- Daily challenges give points
- Weekly challenges give more points
- Secret missions exist
- Leaderboard shows rankings

CHANNELS:
- #🎭・ᴄʜᴏᴏꜱᴇ﹣ʏᴏᴜʀ﹣ʀᴏʟᴇ → choose roles
- #🔥・ᴅᴀɪʟʏ﹣ᴄʜᴀʟʟᴇɴɢᴇ → daily tasks
- #⚡・ᴡᴇᴇᴋʟʏ﹣ᴄʜᴀʟʟᴇɴɢᴇ → weekly tasks

SHOP:
- Users can buy items using points

IMPORTANT:
If information is not in this context, say:
"I don't have information about that in the RUTHLESS server."
"""

# ===== GEMINI FUNCTION =====
def ask_gemini(user_input):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    prompt = f"""
You are a strict English Discord server assistant.

RULES:
- Always respond in English only
- Be short, clear, and helpful
- Only use the server information provided
- Do NOT invent any server data

SERVER CONTEXT:
{SERVER_CONTEXT}

User question:
{user_input}
"""

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(url, json=payload)

    try:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "Sorry, I couldn't process your request right now."


# ===== EVENTS =====
@client.event
async def on_ready():
    print(f"Bot is online as {client.user}")


@client.event
async def on_message(message):
    if message.author.bot:
        return

    # Only one channel
    if message.channel.id != CHANNEL_ID:
        return

    async with message.channel.typing():
        reply = ask_gemini(message.content)
        await message.reply(reply)


# ===== RUN BOT =====
client.run(TOKEN)
