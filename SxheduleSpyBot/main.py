from re import S
from csAutoCompiler import CompileAll
from botBase import bot
from unIdler import StartUnIdler
from changesChecker import StartCheckerLoop
import botCommands


CompileAll()
#StartUnIdler()
#StartCheckerLoop(300)

print("Bot started...")

bot.polling(none_stop=True)