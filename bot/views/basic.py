from telegram import CallbackQuery


async def mensaje(query: CallbackQuery, message: str):
    await query.edit_message_text(text=message)


async def error(query: CallbackQuery, message: str, error: str):
    await mensaje(query, f"{message}: {error}")
