import time
import telebot
import telebot.types as types

from typing import Union, Optional, List
from botEnv import ADMIN_IDS, LOG_CLIENT_API, TELEGRAM_BOT_API


class CustomTeleBot(telebot.TeleBot):
    def __init__(self, token):
        super().__init__(token)

    def ensure_send_message(
        self,
        chat_id: Union[int, str],
        text: str,
        parse_mode: Optional[str] = None,
        entities: Optional[List[types.MessageEntity]] = None,
        disable_web_page_preview: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                types.InlineKeyboardMarkup,
                types.ReplyKeyboardMarkup,
                types.ReplyKeyboardRemove,
                types.ForceReply,
            ]
        ] = None,
        timeout: Optional[int] = None,
        message_thread_id: Optional[int] = None,
        reply_parameters: Optional[types.ReplyParameters] = None,
        link_preview_options: Optional[types.LinkPreviewOptions] = None,
        business_connection_id: Optional[str] = None,
        message_effect_id: Optional[str] = None,
        allow_paid_broadcast: Optional[bool] = None,
    ) -> types.Message:
        while True:
            try:
                self.send_message(
                    chat_id=chat_id,
                    text=text,
                    parse_mode=parse_mode,
                    entities=entities,
                    disable_web_page_preview=disable_web_page_preview,
                    disable_notification=disable_notification,
                    protect_content=protect_content,
                    reply_to_message_id=reply_to_message_id,
                    allow_sending_without_reply=allow_sending_without_reply,
                    reply_markup=reply_markup,
                    timeout=timeout,
                    message_thread_id=message_thread_id,
                    reply_parameters=reply_parameters,
                    link_preview_options=link_preview_options,
                    business_connection_id=business_connection_id,
                    message_effect_id=message_effect_id,
                    allow_paid_broadcast=allow_paid_broadcast,
                )
                break
            except Exception as e:
                if 'Too Many Requests' not in str(e):
                    break
                print(e)
                time.sleep(10)

    def send_messages(
        self,
        chat_ids: List[Union[int, str]],
        text: str,
        parse_mode: Optional[str] = None,
        entities: Optional[List[types.MessageEntity]] = None,
        disable_web_page_preview: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                types.InlineKeyboardMarkup,
                types.ReplyKeyboardMarkup,
                types.ReplyKeyboardRemove,
                types.ForceReply,
            ]
        ] = None,
        timeout: Optional[int] = None,
        message_thread_id: Optional[int] = None,
        reply_parameters: Optional[types.ReplyParameters] = None,
        link_preview_options: Optional[types.LinkPreviewOptions] = None,
        business_connection_id: Optional[str] = None,
        message_effect_id: Optional[str] = None,
        allow_paid_broadcast: Optional[bool] = None,
    ) -> types.Message:
        exceptions = {}

        for chat_id in chat_ids:
            try:
                self.send_message(
                    chat_id=chat_id,
                    text=text,
                    parse_mode=parse_mode,
                    entities=entities,
                    disable_web_page_preview=disable_web_page_preview,
                    disable_notification=disable_notification,
                    protect_content=protect_content,
                    reply_to_message_id=reply_to_message_id,
                    allow_sending_without_reply=allow_sending_without_reply,
                    reply_markup=reply_markup,
                    timeout=timeout,
                    message_thread_id=message_thread_id,
                    reply_parameters=reply_parameters,
                    link_preview_options=link_preview_options,
                    business_connection_id=business_connection_id,
                    message_effect_id=message_effect_id,
                    allow_paid_broadcast=allow_paid_broadcast,
                )
            except Exception as e:
                exceptions[str(chat_id)] = e
        if len(exceptions) != 0:
            raise Exception(
                '\n'.join(
                    [
                        f'Chat ID {chat_id}:\n{exception}'
                        for chat_id, exception in exceptions.items()
                    ]
                )
            )

    def ensure_send_messages(
        self,
        chat_ids: List[Union[int, str]],
        text: str,
        parse_mode: Optional[str] = None,
        entities: Optional[List[types.MessageEntity]] = None,
        disable_web_page_preview: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                types.InlineKeyboardMarkup,
                types.ReplyKeyboardMarkup,
                types.ReplyKeyboardRemove,
                types.ForceReply,
            ]
        ] = None,
        timeout: Optional[int] = None,
        message_thread_id: Optional[int] = None,
        reply_parameters: Optional[types.ReplyParameters] = None,
        link_preview_options: Optional[types.LinkPreviewOptions] = None,
        business_connection_id: Optional[str] = None,
        message_effect_id: Optional[str] = None,
        allow_paid_broadcast: Optional[bool] = None,
    ) -> types.Message:
        exceptions = {}

        for chat_id in chat_ids:
            while True:
                try:
                    self.send_message(
                        chat_id=chat_id,
                        text=text,
                        parse_mode=parse_mode,
                        entities=entities,
                        disable_web_page_preview=disable_web_page_preview,
                        disable_notification=disable_notification,
                        protect_content=protect_content,
                        reply_to_message_id=reply_to_message_id,
                        allow_sending_without_reply=allow_sending_without_reply,
                        reply_markup=reply_markup,
                        timeout=timeout,
                        message_thread_id=message_thread_id,
                        reply_parameters=reply_parameters,
                        link_preview_options=link_preview_options,
                        business_connection_id=business_connection_id,
                        message_effect_id=message_effect_id,
                        allow_paid_broadcast=allow_paid_broadcast,
                    )
                    break
                except Exception as e:
                    if 'Too Many Requests' not in str(e):
                        exceptions[str(chat_id)] = e
                        break
                    time.sleep(10)

        return exceptions


try:
    adminIds = ADMIN_IDS.split(',')
    adminIds = [int(item) for item in adminIds if item.isdigit()]
except Exception:
    adminIds = []
    pass


bot = CustomTeleBot(TELEGRAM_BOT_API)
logClient = CustomTeleBot(LOG_CLIENT_API)
