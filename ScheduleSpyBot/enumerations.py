from enum import Enum

class WeekDay(Enum):
    Понеділок = 0
    Вівторок  = 1
    Середа    = 2
    Четвер    = 3
    Пятниця   = 4
    Субота    = 5
    Неділя    = 6

class Group(Enum):
    KC241_1 = 'C'
    KC241_2 = 'D'
    KC242_1 = 'E'
    KC242_2 = 'F'
    KN24_1  = 'G'
    KN24_2  = 'H'
    KT24    = 'I'

class Notifier(Enum):
    KC241_1 = 4648
    KC241_2 = 4652
    KC242_1 = 4655
    KC242_2 = 4656
    KN24_1  = 4657
    KN24_2  = 4658
    KT24    = 4659

notifierToGroup = {
Notifier.KC241_1: Group.KC241_1,
Notifier.KC241_2: Group.KC241_2,
Notifier.KC242_1: Group.KC242_1,
Notifier.KC242_2: Group.KC242_2,
Notifier.KN24_1 : Group.KN24_1,
Notifier.KN24_2 : Group.KN24_2,
Notifier.KT24   : Group.KT24}


