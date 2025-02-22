import os
import time
import telebot
import telebot.types as types
from dotenv import load_dotenv
from testModeVariable import TEST_MODE
from typing import Union, Optional, List


current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '..', 'Secrets', 'KEYS.env')
load_dotenv(env_path)

class CustomTeleBot(telebot.TeleBot):
    def __init__(self, token):
        super().__init__(token)

    def garanted_send_message(
            self, chat_id: Union[int, str], text: str, 
            parse_mode: Optional[str]=None, 
            entities: Optional[List[types.MessageEntity]]=None,
            disable_web_page_preview: Optional[bool]=None,
            disable_notification: Optional[bool]=None, 
            protect_content: Optional[bool]=None,
            reply_to_message_id: Optional[int]=None,
            allow_sending_without_reply: Optional[bool]=None,
            reply_markup: Optional[Union[types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, types.ReplyKeyboardRemove, types.ForceReply]]=None,
            timeout: Optional[int]=None,
            message_thread_id: Optional[int]=None,
            reply_parameters: Optional[types.ReplyParameters]=None,
            link_preview_options : Optional[types.LinkPreviewOptions]=None,
            business_connection_id: Optional[str]=None,
            message_effect_id: Optional[str]=None,
            allow_paid_broadcast: Optional[bool]=None) -> types.Message:
        
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
                    allow_paid_broadcast=allow_paid_broadcast)
                break
            except Exception as e:
                if not ("Too Many Requests" in str(e)):
                    break
                print(e) 
                time.sleep(10)

    def send_messages(
            self, chat_ids: List[Union[int, str]], text: str, 
            parse_mode: Optional[str]=None, 
            entities: Optional[List[types.MessageEntity]]=None,
            disable_web_page_preview: Optional[bool]=None,
            disable_notification: Optional[bool]=None, 
            protect_content: Optional[bool]=None,
            reply_to_message_id: Optional[int]=None,
            allow_sending_without_reply: Optional[bool]=None,
            reply_markup: Optional[Union[types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, types.ReplyKeyboardRemove, types.ForceReply]]=None,
            timeout: Optional[int]=None,
            message_thread_id: Optional[int]=None,
            reply_parameters: Optional[types.ReplyParameters]=None,
            link_preview_options : Optional[types.LinkPreviewOptions]=None,
            business_connection_id: Optional[str]=None,
            message_effect_id: Optional[str]=None,
            allow_paid_broadcast: Optional[bool]=None) -> types.Message:  

        exeptions = {}

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
                            allow_paid_broadcast=allow_paid_broadcast)
            except Exception as e:
                exeptions[str(chat_id)] = e
        if len(exeptions) != 0:
            raise Exception("\n".join([f"Chat ID {chat_id}:\n{exeption}" for chat_id, exeption in exeptions.items()]))

    def garanted_send_messages(
            self, chat_ids: List[Union[int, str]], text: str, 
            parse_mode: Optional[str]=None, 
            entities: Optional[List[types.MessageEntity]]=None,
            disable_web_page_preview: Optional[bool]=None,
            disable_notification: Optional[bool]=None, 
            protect_content: Optional[bool]=None,
            reply_to_message_id: Optional[int]=None,
            allow_sending_without_reply: Optional[bool]=None,
            reply_markup: Optional[Union[types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, types.ReplyKeyboardRemove, types.ForceReply]]=None,
            timeout: Optional[int]=None,
            message_thread_id: Optional[int]=None,
            reply_parameters: Optional[types.ReplyParameters]=None,
            link_preview_options : Optional[types.LinkPreviewOptions]=None,
            business_connection_id: Optional[str]=None,
            message_effect_id: Optional[str]=None,
            allow_paid_broadcast: Optional[bool]=None) -> types.Message:
        

        exeptions = {}

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
                        allow_paid_broadcast=allow_paid_broadcast)
                    break
                except Exception as e:
                    if not ("Too Many Requests" in str(e)):
                        exeptions[str(chat_id)] = e
                        break                                         
                    time.sleep(10)

        return exeptions

try:
    ADMIN_IDS = os.getenv("ADMIN_IDS")
    adminIds = ADMIN_IDS.split(",")
    adminIds = [int(item) for item in adminIds if item.isdigit()]
except Exception as e:
    adminIds = []
    pass

if not TEST_MODE:
    TELEGRAM_BOT_API = os.getenv("BOT_API")
else:
    TELEGRAM_BOT_API = os.getenv("BOT_API_T")

LOG_CLIENT_API = os.getenv("LOG_CLIENT_API")
bot       = CustomTeleBot(TELEGRAM_BOT_API)
logClient = CustomTeleBot(LOG_CLIENT_API)       
            