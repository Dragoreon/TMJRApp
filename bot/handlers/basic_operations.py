from telegram import InlineKeyboardButton


def new_button(text: str, callback_name: str) -> InlineKeyboardButton:
    """Helper function to create a button."""
    return InlineKeyboardButton(text, callback_data=callback_name)
