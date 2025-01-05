from csAutoCompiler import CompileAll
CompileAll()

from botBase import bot
from changesChecker import StartCheckerLoop
import botCommands

print("Bot started...")

StartCheckerLoop(120) 

bot.polling(none_stop=True)