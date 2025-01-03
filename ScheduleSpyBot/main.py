from csAutoCompiler import CompileAll
CompileAll()

from botBase import bot
from unIdler import StartUnIdler
from changesChecker import StartCheckerLoop
import botCommands

print("Bot started...")

StartUnIdler()
StartCheckerLoop(300) 

bot.polling(none_stop=True)