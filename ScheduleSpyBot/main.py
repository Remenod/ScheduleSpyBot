from botBase import bot
from changesChecker import StartCheckerLoop
import botCommands

print("Bot started...")

StartCheckerLoop(480) 

bot.polling(none_stop=True)