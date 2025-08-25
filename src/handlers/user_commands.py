from typing import Any

from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command

from database import db

router = Router()


@router.message(CommandStart())
async def start(message: Message, user: dict[str, Any]) -> None:
    # Check if it's a deep link (someone clicking on user's anonymous link)
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    
    if args:
        # Someone is trying to send an anonymous message
        target_code = args[0]
        target_user = await db.get_user_by_code(target_code)
        
        if target_user:
            await message.reply(
                f"💬 <b>Send an anonymous message!</b>\n\n"
                f"Write your message and it will be sent anonymously. "
                f"The recipient won't know who sent it.",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="❌ Cancel", callback_data=f"cancel_{target_code}")]
                ])
            )
            # Store the target for this user's next message
            await db.update_user(message.from_user.id, pending_target=target_code)
        else:
            await message.reply("❌ Invalid link or user not found.")
    else:
        # Regular start - show user their anonymous link
        bot_username = (await message.bot.get_me()).username
        user_link = f"https://t.me/{bot_username}?start={user['unique_code']}"
        
        await message.reply(
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