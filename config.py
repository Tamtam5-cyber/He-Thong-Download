import os
from dotenv import load_dotenv

load_dotenv()

# VPS --- FILL COOKIES 🍪 in """ ... """ 

INST_COOKIES = """
# wtite up here insta cookies
"""

YTUB_COOKIES = """
# write here yt cookies
"""

API_ID = os.getenv("API_ID", "24523730")
API_HASH = os.getenv("API_HASH", "c7425e424447932cc25ec8f43a7fbc2d")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7537588681:AAHy45ORqyArvg0nhVo8H8KqQlae2oSNG40")
MONGO_DB = os.getenv("MONGO_DB", "mongodb+srv://nguyenkhactam5:q1231234@superbot.vmvzlsu.mongodb.net/?retryWrites=true&w=majority&appName=SuperBot")
OWNER_ID = list(map(int, os.getenv("OWNER_ID", "6798798180").split())) # list seperated via space
DB_NAME = os.getenv("DB_NAME", "nguyenkhactam5")
STRING = os.getenv("STRING", None) # optional
LOG_GROUP = int(os.getenv("LOG_GROUP", "-1002283092497")) # optional with -100
FORCE_SUB = int(os.getenv("FORCE_SUB", "-1002472444792")) # optional with -100
MASTER_KEY = os.getenv("MASTER_KEY", "d070f1fbcadc95a18b2e8e68512f76fe") # for session encryption
IV_KEY = os.getenv("IV_KEY", "83eceaf60418") # for decryption
YT_COOKIES = os.getenv("YT_COOKIES", YTUB_COOKIES)
INSTA_COOKIES = os.getenv("INSTA_COOKIES", INST_COOKIES)
FREEMIUM_LIMIT = int(os.getenv("FREEMIUM_LIMIT", "10"))
PREMIUM_LIMIT = int(os.getenv("PREMIUM_LIMIT", "100"))
JOIN_LINK = os.getenv("JOIN_LINK", "https://t.me/ULTIMATESMMNEWS") # this link for start command message
ADMIN_CONTACT = os.getenv("ADMIN_CONTACT", "https://t.me/Name_Apex")
