from csAutoCompiler import CompileAll
CompileAll()

from botBase import bot
from unIdler import StartUnIdler
from changesChecker import StartCheckerLoop
import botCommands

#StartUnIdler()
#StartCheckerLoop(300) 

print("Bot started...")

bot.polling(none_stop=True)