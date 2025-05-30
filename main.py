import asyncio
from shared_client import start_client
import importlib
import os
import sys
from utils.func import check_mongo_connection
from plugins import batch
import signal
import sys
import asyncio
from pyrogram import idle

async def main():
    # Khởi động bot
    print("Bot is starting...")
    await idle()  # Giữ bot chạy

def signal_handler(sig, frame):
    print("Bot is shutting down gracefully...")
    loop = asyncio.get_event_loop()
    loop.stop()
    sys.exit(0)

if __name__ == "__main__":
    # Đăng ký xử lý tín hiệu
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Chạy bot
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
async def start_plugins():
    await batch.run_batch_plugin()
async def load_and_run_plugins():
    global client, app, userbot
    try:
        client, app, userbot = await start_client()
    except Exception as e:
        print(f"Failed to start clients: {e}")
        sys.exit(1)

    # Kiểm tra kết nối MongoDB
    await check_mongo_connection()

    plugin_dir = "plugins"
    plugins = [f[:-3] for f in os.listdir(plugin_dir) if f.endswith(".py") and f != "__init__.py"]

    for plugin in plugins:
        try:
            module = importlib.import_module(f"plugins.{plugin}")
            if hasattr(module, f"run_{plugin}_plugin"):
                print(f"Running {plugin} plugin...")
                await getattr(module, f"run_{plugin}_plugin")()
            else:
                print(f"Plugin {plugin} does not have run_{plugin}_plugin function")
        except Exception as e:
            print(f"Error running plugin {plugin}: {e}")

    return client, app, userbot

async def main():
    try:
        client, app, userbot = await load_and_run_plugins()
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        try:
            # Dừng các tác vụ Pyrogram
            if app:
                app.dispatcher.stop()
                await app.stop()
                print("Pyrogram client stopped.")
            # Dừng Telethon client
            if client and client.is_connected():
                await client.disconnect()
                print("Telethon client stopped.")
            if userbot and userbot.is_connected():
                await userbot.stop()
                print("Userbot stopped.")
        except Exception as e:
            print(f"Error stopping clients: {e}")
        finally:
            # Đảm bảo thoát chương trình
            sys.exit(0)

if __name__ == "__main__":
    print("Starting clients ...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped by user.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
