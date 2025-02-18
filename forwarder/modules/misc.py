from telegram import Bot, ParseMode, Update
from telegram.ext import Filters, MessageHandler

from forwarder import FROM_CHATS, OWNER_ID, TO_CHATS, dispatcher


def get_id(update, context):
    message = update.effective_message  # type: Optional[Message]

    if message.reply_to_message:  # Message is a reply to another message
        if (
            message.reply_to_message.forward_from
        ):  # Replied message is a forward from a user
            sender = message.reply_to_message.forward_from
            forwarder = message.reply_to_message.from_user
            message.reply_text(
                "Tʜᴇ Oʀɪɢɪɴᴀʟ Sᴇɴᴅᴇʀ, {}, Hᴀs Aɴ Iᴅ Oғ `{}`. \n"
                "Tʜᴇ Fᴏʀᴡᴀʀᴅᴇʀ, {}, Hᴀs Aɴ Iᴅ Oғ `{}`.".format(
                    sender.first_name, sender.id, forwarder.first_name, forwarder.id
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
        elif (
            message.reply_to_message.forward_from_chat
        ):  # Replied message is a forward from a channel
            channel = message.reply_to_message.forward_from_chat
            forwarder = message.reply_to_message.from_user
            message.reply_text(
                "Tʜᴇ Cʜᴀɴɴᴇʟ, {}, Hᴀs Aɴ Iᴅ Oғ `{}`. \n"
                "Tʜᴇ Fᴏʀᴡᴀʀᴅᴇʀ, {}, Hᴀs Aɴ Iᴅ Oғ `{}`.".format(
                    channel.title, channel.id, forwarder.first_name, forwarder.id
                ),
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            user = (
                message.reply_to_message.from_user
            )  # Replied message is a message from a user
            message.reply_text(
                "{}'s Iᴅ Is `{}`.".format(user.first_name, user.id),
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        chat = update.effective_chat

        if chat.type == "private":  # Private chat with the bot
            message.reply_text(
                "Yᴏᴜʀ Iᴅ Is `{}`.".format(chat.id), parse_mode=ParseMode.MARKDOWN
            )

        else:  # Group chat where the bot is a member
            message.reply_text(
                "Tʜɪs Gʀᴏᴜᴘ Iᴅ  `{}`.".format(chat.id),
                parse_mode=ParseMode.MARKDOWN,
            )


GET_ID_HANDLER = MessageHandler(
    Filters.command
    & Filters.regex(r"^/id")
    & (Filters.user(OWNER_ID) | Filters.update.channel_posts),
    get_id,
    run_async=True,
)

dispatcher.add_handler(GET_ID_HANDLER)
