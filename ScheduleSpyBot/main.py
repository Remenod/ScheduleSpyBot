from csAutoCompiler import CompileAll
CompileAll()

from botBase import bot
from unIdler import StartUnIdler
from changesChecker import StartCheckerLoop
import botCommands

print("Bot started...")


bot.polling(none_stop=True)