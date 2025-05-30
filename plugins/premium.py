from shared_client import client as bot_client, app
from telethon import events
from datetime import timedelta, datetime
from config import OWNER_ID, FORCE_SUB, JOIN_LINK as JL, ADMIN_CONTACT as AC
from utils.func import add_premium_user, is_private_chat, initialize_user_tasks, get_user_tasks, update_task_status, get_user_data
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton as IK, InlineKeyboardMarkup as IKM
from pyrogram.errors import UserNotParticipant
import base64 as spy
from plugins.start import subscribe

# Các chuỗi mã hóa (giả định từ utils/func.py)
a1 = "c2F2ZV9yZXN0cmljdGVkX2NvbnRlbnRfYm90cw=="
a2 = "Nzk2"
a3 = "Z2V0X21lc3NhZ2Vz"
a4 = "cmVwbHlfcGhvdG8="
a5 = "c3RhcnQ="
attr1 = spy.b64encode("photo".encode()).decode()
attr2 = spy.b64encode("file_id".encode()).decode()
a7 = "SGkg8J+RiyBXZWxjb21lLCBXYW5uYSBpbnRyby4uLj8gCgrinLPvuI8gSSBjYW4gc2F2ZSBwb3N0cyBmcm9tIGNoYW5uZWxzIG9yIGdyb3VwcyB3aGVyZSBmb3J3YXJkaW5nIGlzIG9mZi4gSSBjYW4gZG93bmxvYWQgdmlkZW9zL2F1ZGlvIGZyb20gWVQsIElOU1RBLCAuLi4gc29jaWFsIHBsYXRmb3JtcwrinLPvuI8gU2ltcGx5IHNlbmQgdGhlIHBvc3QgbGluayBvZiBhIHB1YmxpYyBjaGFubmVsLiBGb3IgcHJpdmF0ZSBjaGFubmVscywgZG8gL2xvZ2luLiBTZW5kIC9oZWxwIHRvIGtub3cgbW9yZS4="
a8 = "Sm9pbiBDaGFubmVs"
a9 = "R2V0IFByZW1pdW0="

@bot_client.on(events.NewMessage(pattern='/add'))
async def add_premium_handler(event):
    if not await is_private_chat(event):
        await event.respond('This command can only be used in private chats for security reasons.')
        return
    user_id = event.sender_id
    if user_id not in OWNER_ID:
        await event.respond('This command is restricted to the bot owner.')
        return
    text = event.message.text.strip()
    parts = text.split(' ')
    if len(parts) != 4:
        await event.respond(
            """Invalid format. Use: /add user_id duration_value duration_unit
Example: /add 123456 1 week"""
        )
        return
    try:
        target_user_id = int(parts[1])
        duration_value = int(parts[2])
        duration_unit = parts[3].lower()
        valid_units = ['min', 'hours', 'days', 'weeks', 'month', 'year', 'decades']
        if duration_unit not in valid_units:
            await event.respond(f"Invalid duration unit. Choose from: {', '.join(valid_units)}")
            return
        success, result = await add_premium_user(target_user_id, duration_value, duration_unit)
        if success:
            expiry_utc = result
            expiry_ist = expiry_utc + timedelta(hours=5, minutes=30)
            formatted_expiry = expiry_ist.strftime('%d-%b-%Y %I:%M:%S %p')
            await event.respond(
                f"""✅ User {target_user_id} added as premium member
Subscription valid until: {formatted_expiry} (IST)"""
            )
            await bot_client.send_message(
                target_user_id,
                f"""✅ You have been added as a premium member
**Validity until**: {formatted_expiry} (IST)"""
            )
        else:
            await event.respond(f'❌ Failed to add premium user: {result}')
    except ValueError:
        await event.respond('Invalid user ID or duration value. Both must be integers.')
    except Exception as e:
        await event.respond(f'Error: {str(e)}')

@app.on_message(filters.command(spy.b64decode(a5.encode()).decode()))
async def start_handler(client, message):
    print("Received /start command")
    try:
        print("Checking subscription status...")
        subscription_status = await subscribe(client, message)
        if subscription_status == 1:
            print("Subscription status = 1, user needs to subscribe.")
            return
        user = message.from_user
        user_id = user.id
        first_name = user.first_name or "Không có tên"
        username = f"@{user.username}" if user.username else "Không có username"
        print(f"User info: ID={user_id}, Name={first_name}, Username={username}")

        print("Initializing user tasks...")
        await initialize_user_tasks(user_id)
        tasks = await get_user_tasks(user_id)
        print(f"Tasks: {tasks}")

        try:
            print("Checking channel membership...")
            channel_member = await app.get_chat_member(FORCE_SUB, user_id)
            if channel_member:
                await update_task_status(user_id, "join_channel", "completed")
                print("User joined channel, updated task status")
            else:
                print("User not in channel")
        except UserNotParticipant:
            await update_task_status(user_id, "join_channel", "pending")
            print("UserNotParticipant, set join_channel to pending")
            await message.reply_text("Vui lòng tham gia kênh để sử dụng bot!", reply_markup=IKM([[IK("Join Channel", url=JL)]]))
            return
        except Exception as e:
            print(f"Error checking channel membership: {e}")
            await update_task_status(user_id, "join_channel", "pending")

        print("Fetching user data...")
        user_data = await get_user_data(user_id)
        print(f"User data: {user_data}")

        if user_data and "session_string" in user_data and user_data["session_string"]:
            await update_task_status(user_id, "login", "completed")
            print("User logged in, updated task status")
        else:
            await update_task_status(user_id, "login", "pending")
            print("User not logged in, set login to pending")

        if user_data and "bot_token" in user_data and user_data["bot_token"]:
            await update_task_status(user_id, "set_custom_bot", "completed")
            print("Custom bot set, updated task status")
        else:
            await update_task_status(user_id, "set_custom_bot", "pending")
            print("Custom bot not set, set to pending")

        tasks = await get_user_tasks(user_id)
        task_list = [
            f"- [{'✅' if tasks['join_channel'] == 'completed' else ' '}] Tham gia kênh",
            f"- [{'✅' if tasks['login'] == 'completed' else ' '}] Đăng nhập vào bot",
            f"- [{'✅' if tasks['set_custom_bot'] == 'completed' else ' '}] Thiết lập bot tùy chỉnh"
        ]
        print("Generating caption...")
        b6 = spy.b64decode(a7).decode()
        caption = (
            f"**Thông tin của bạn:**\n"
            f"👤 Tên: {first_name}\n"
            f"🆔 ID: {user_id}\n"
            f"❇️ Username: {username}\n\n"
            f"**Danh sách nhiệm vụ:**\n" + "\n".join(task_list) + "\n\n"
            f"{b6}"
        )
        b7 = spy.b64decode(a8).decode()
        b8 = spy.b64decode(a9).decode()
        kb = IKM([
            [IK(b7, url=JL)],
            [IK(b8, url=AC)]
        ])

        try:
            print("Checking user photo...")
            photo_file_id = None
            if user.photo and hasattr(user.photo, 'big_file_id'):
                photo_file_id = user.photo.big_file_id
                print(f"Sending photo: {photo_file_id}")
                await message.reply_photo(
                    photo=photo_file_id,
                    caption=caption,
                    reply_markup=kb
                )
                print("Photo sent successfully")
            else:
                raise AttributeError("User photo not available or not a PHOTO")
        except Exception as e:
            print(f"Error sending user photo: {e}")
            try:
                print("Fetching default photo...")
                b1 = spy.b64decode(a1).decode()
                b2 = int(spy.b64decode(a2).decode())
                b3 = spy.b64decode(a3).decode()
                b4 = spy.b64decode(a4).decode()
                tm = await getattr(app, b3)(b1, b2)
                pb = getattr(tm, spy.b64decode(attr1.encode()).decode())
                fd = getattr(pb, spy.b64decode(attr2.encode()).decode())
                print(f"Sending default photo: {fd}")
                await getattr(message, b4)(
                    fd,
                    caption=caption + "\n\nℹ️ Bạn chưa có ảnh đại diện, hiển thị ảnh mặc định.",
                    reply_markup=kb
                )
                print("Default photo sent successfully")
            except Exception as e:
                print(f"Error sending default photo: {e}")
                await message.reply_text(
                    caption + f"\n\n⚠️ Bạn chưa có ảnh đại diện và ảnh mặc định không tải được: {str(e)[:50]}",
                    reply_markup=kb
                )
    except Exception as e:
        await message.reply_text(
            f"⚠️ Đã xảy ra lỗi nghiêm trọng: {str(e)[:50]}\nVui lòng liên hệ admin để được hỗ trợ.",
            reply_markup=kb
        )

# Hàm khởi tạo plugin
async def run_premium_plugin():
    print("Premium plugin initialized successfully")
