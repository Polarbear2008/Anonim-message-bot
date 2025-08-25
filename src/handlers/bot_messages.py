from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from config_reader import is_admin_user, config

router = Router()


# Removed old chat functionality - not needed for anonymous message bot


# Old handler removed - using handle_anonymous_message instead


@router.callback_query(F.data.startswith("cancel_"))
async def cancel_anonymous_message(callback: CallbackQuery) -> None:
    """Cancel sending anonymous message"""
    await db.update_user(callback.from_user.id, pending_target=None)
    await callback.message.edit_text("❌ Cancelled. You can start over anytime.")
    await callback.answer()


@router.callback_query(F.data == "stats")
async def show_stats(callback: CallbackQuery, user: dict) -> None:
    """Show user statistics"""
    await callback.message.edit_text(
        f"📊 <b>Your Statistics</b>\n\n"
        f"💬 Messages received: <b>{user['message_count']}</b>\n"
        f"🔗 Your unique code: <code>{user['unique_code']}</code>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_main")]
        ])
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery, user: dict) -> None:
    """Go back to main menu"""
    bot_username = (await callback.bot.get_me()).username
    user_link = f"https://t.me/{bot_username}?start={user['unique_code']}"
    
    await callback.message.edit_text(
        f"🚀 <b>Start receiving anonymous messages right now!</b>\n\n"
        f"Your link:\n"
        f"👉 <code>{user_link}</code>\n\n"
        f"Add this link ☝️ to your Telegram/TikTok/Instagram bio, to start receiving anonymous messages 💬\n\n"
        f"📊 Messages received: <b>{user['message_count']}</b>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔗 Share link", url=f"https://t.me/share/url?url={user_link}")],
            [InlineKeyboardButton(text="📊 Statistics", callback_data="stats")]
        ])
    )
    await callback.answer()


@router.message(F.content_type.in_(["text", "photo", "video", "voice", "audio", "document", "sticker"]))
async def handle_anonymous_message(message: Message, user: dict) -> None:
    """Handle incoming messages that should be sent anonymously"""
    
    # Check if user has a pending target (someone to send anonymous message to)
    if user.get('pending_target'):
        target_user = await db.get_user_by_code(user['pending_target'])
        
        if target_user:
            # Get sender username for display
            sender_username = message.from_user.username or message.from_user.first_name or "Unknown"
            
            # Send combined notification and message (show username only to admin users)
            if message.content_type == "text":
                if is_admin_user(target_user['id']):
                    header = f"🍿 <b>@{sender_username} sent you an anonymous message!</b>"
                else:
                    header = "🍿 <b>Someone sent you an anonymous message!</b>"
                sent_msg = await message.bot.send_message(
                    target_user['id'], 
                    f"{header}\n\n{message.text}\n\n↩️ <i>Just swipe to reply.</i>"
                )
            elif message.content_type == "photo":
                if is_admin_user(target_user['id']):
                    caption = f"🍿 <b>@{sender_username} sent you an anonymous message!</b>\n\n{message.caption or ''}\n\n↩️ <i>Just swipe to reply.</i>"
                else:
                    caption = f"🍿 <b>Someone sent you an anonymous message!</b>\n\n{message.caption or ''}\n\n↩️ <i>Just swipe to reply.</i>"
                sent_msg = await message.bot.send_photo(target_user['id'], message.photo[-1].file_id, caption=caption)
            elif message.content_type == "video":
                if is_admin_user(target_user['id']):
                    caption = f"🍿 <b>@{sender_username} sent you an anonymous message!</b>\n\n{message.caption or ''}\n\n↩️ <i>Just swipe to reply.</i>"
                else:
                    caption = f"🍿 <b>Someone sent you an anonymous message!</b>\n\n{message.caption or ''}\n\n↩️ <i>Just swipe to reply.</i>"
                sent_msg = await message.bot.send_video(target_user['id'], message.video.file_id, caption=caption)
            elif message.content_type == "voice":
                if is_admin_user(target_user['id']):
                    voice_header = f"🍿 <b>@{sender_username} sent you an anonymous voice message!</b>"
                else:
                    voice_header = "🍿 <b>Someone sent you an anonymous voice message!</b>"
                sent_msg = await message.bot.send_message(
                    target_user['id'],
                    f"{voice_header}\n\n↩️ <i>Just swipe to reply.</i>"
                )
                await message.bot.send_voice(target_user['id'], message.voice.file_id)
            elif message.content_type == "audio":
                if is_admin_user(target_user['id']):
                    caption = f"🍿 <b>@{sender_username} sent you an anonymous message!</b>\n\n{message.caption or ''}\n\n↩️ <i>Just swipe to reply.</i>"
                else:
                    caption = f"🍿 <b>Someone sent you an anonymous message!</b>\n\n{message.caption or ''}\n\n↩️ <i>Just swipe to reply.</i>"
                sent_msg = await message.bot.send_audio(target_user['id'], message.audio.file_id, caption=caption)
            elif message.content_type == "document":
                if is_admin_user(target_user['id']):
                    caption = f"🍿 <b>@{sender_username} sent you an anonymous message!</b>\n\n{message.caption or ''}\n\n↩️ <i>Just swipe to reply.</i>"
                else:
                    caption = f"🍿 <b>Someone sent you an anonymous message!</b>\n\n{message.caption or ''}\n\n↩️ <i>Just swipe to reply.</i>"
                sent_msg = await message.bot.send_document(target_user['id'], message.document.file_id, caption=caption)
            elif message.content_type == "sticker":
                if is_admin_user(target_user['id']):
                    sticker_header = f"🍿 <b>@{sender_username} sent you an anonymous sticker!</b>"
                else:
                    sticker_header = "🍿 <b>Someone sent you an anonymous sticker!</b>"
                sent_msg = await message.bot.send_message(
                    target_user['id'],
                    f"{sticker_header}\n\n↩️ <i>Just swipe to reply.</i>"
                )
                await message.bot.send_sticker(target_user['id'], message.sticker.file_id)
            
            # Store message record for reply functionality with sender username
            await db.create_message_record(message.from_user.id, target_user['id'], sent_msg.message_id, sender_username)
            # Also store the reverse mapping for reply chains
            await db.create_message_record(target_user['id'], message.from_user.id, sent_msg.message_id, sender_username)
            
            # Forward to log group if configured
            if config.LOG_GROUP_ID:
                try:
                    log_text = f"📝 <b>Anonymous Message Log</b>\n\n"
                    log_text += f"👤 <b>From:</b> @{sender_username} (ID: {message.from_user.id})\n"
                    log_text += f"👥 <b>To:</b> {target_user.get('first_name', 'Unknown')} (ID: {target_user['id']})\n"
                    log_text += f"💬 <b>Message:</b> {message.text if message.content_type == 'text' else f'{message.content_type.upper()} message'}\n"
                    log_text += f"🕐 <b>Time:</b> {message.date.strftime('%Y-%m-%d %H:%M:%S')}"
                    
                    await message.bot.send_message(int(config.LOG_GROUP_ID), log_text)
                except Exception as e:
                    print(f"Failed to send to log group: {e}")
            
            # Increment message count for target user
            await db.increment_message_count(target_user['id'])
            
            # Clear pending target
            await db.update_user(message.from_user.id, pending_target=None)
            
            # Confirm to sender
            await message.reply("✅ Your anonymous message has been sent!")
        else:
            await message.reply("❌ Target user not found. Please try again.")
            await db.update_user(message.from_user.id, pending_target=None)
    else:
        # Check if this is a reply to an anonymous message
        if message.reply_to_message and message.reply_to_message.from_user.is_bot:
            # Get message info to determine who is the link owner
            message_info = await db.get_message_info(message.reply_to_message.message_id)
            
            if message_info:
                original_sender_id = message_info['sender_id']
                original_receiver_id = message_info['receiver_id']
                reply_sender_username = message.from_user.username or message.from_user.first_name or "Unknown"
                
                # Determine if the person replying is the link owner (original receiver)
                # If current user is the original receiver, they are the link owner
                is_link_owner = (message.from_user.id == original_receiver_id)
                
                # Send reply back to the other person
                target_id = original_sender_id if is_link_owner else original_receiver_id
                
                # Format message based on who is receiving it
                # Show username only to admin users
                if is_admin_user(target_id):
                    # Message going to admin - show username
                    reply_header = f"💬 <b>@{reply_sender_username} replied to your anonymous message!</b>"
                else:
                    # Message going to regular user - keep anonymous
                    reply_header = "💬 <b>Someone replied to your anonymous message!</b>"
                
                # Send anonymous reply back
                if message.content_type == "text":
                    reply_msg = await message.bot.send_message(
                        target_id,
                        f"{reply_header}\n\n{message.text}\n\n↩️ <i>Just swipe to reply.</i>"
                    )
                elif message.content_type == "photo":
                    caption = f"{reply_header}\n\n{message.caption or ''}\n\n↩️ <i>Just swipe to reply.</i>"
                    reply_msg = await message.bot.send_photo(target_id, message.photo[-1].file_id, caption=caption)
                elif message.content_type == "video":
                    caption = f"{reply_header}\n\n{message.caption or ''}\n\n↩️ <i>Just swipe to reply.</i>"
                    reply_msg = await message.bot.send_video(target_id, message.video.file_id, caption=caption)
                elif message.content_type == "voice":
                    if is_admin_user(target_id):
                        voice_header = f"💬 <b>@{reply_sender_username} replied with a voice message!</b>"
                    else:
                        voice_header = "💬 <b>Someone replied with a voice message!</b>"
                    reply_msg = await message.bot.send_message(
                        target_id,
                        f"{voice_header}\n\n↩️ <i>Just swipe to reply.</i>"
                    )
                    await message.bot.send_voice(target_id, message.voice.file_id)
                elif message.content_type == "sticker":
                    if is_admin_user(target_id):
                        sticker_header = f"💬 <b>@{reply_sender_username} replied with a sticker!</b>"
                    else:
                        sticker_header = "💬 <b>Someone replied with a sticker!</b>"
                    reply_msg = await message.bot.send_message(
                        target_id,
                        f"{sticker_header}\n\n↩️ <i>Just swipe to reply.</i>"
                    )
                    await message.bot.send_sticker(target_id, message.sticker.file_id)
                
                # Store the reply message for future reply chains
                # Keep the original sender/receiver roles for proper username display
                if is_link_owner:
                    # Link owner replied - store with original roles
                    await db.create_message_record(message.from_user.id, target_id, reply_msg.message_id, reply_sender_username)
                    await db.create_message_record(target_id, message.from_user.id, reply_msg.message_id, reply_sender_username)
                else:
                    # Original sender replied - store with original roles maintained
                    await db.create_message_record(message.from_user.id, target_id, reply_msg.message_id, reply_sender_username)
                    await db.create_message_record(target_id, message.from_user.id, reply_msg.message_id, reply_sender_username)
                
                # Forward reply to log group if configured
                if config.LOG_GROUP_ID:
                    try:
                        log_text = f"💬 <b>Anonymous Reply Log</b>\n\n"
                        log_text += f"👤 <b>From:</b> @{reply_sender_username} (ID: {message.from_user.id})\n"
                        log_text += f"👥 <b>To:</b> ID: {target_id}\n"
                        log_text += f"💬 <b>Reply:</b> {message.text if message.content_type == 'text' else f'{message.content_type.upper()} message'}\n"
                        log_text += f"🕐 <b>Time:</b> {message.date.strftime('%Y-%m-%d %H:%M:%S')}"
                        
                        await message.bot.send_message(int(config.LOG_GROUP_ID), log_text)
                    except Exception as e:
                        print(f"Failed to send reply to log group: {e}")
                
                await message.reply("✅ Your anonymous reply has been sent!")
            else:
                await message.reply("❌ Cannot find the original sender. The message might be too old.")
        else:
            # No pending target, show help
            await message.reply(
                "💡 <b>How to use this bot:</b>\n\n"
                "1. Share your unique link with others\n"
                "2. When someone clicks your link, they can send you anonymous messages\n"
                "3. Use /start to get your link again"
            )
