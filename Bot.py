from schedules import *
import cfg
from datetime import datetime
import telebot
from arg import *
from dateutil.tz import tzoffset
from groups import group

dots = "........................"
def chooseSched(groupNumb):

    for i in group:
        for j in range(len(group[i])):
            if str(group[i][j]) == str(groupNumb):

                print(groupNumb)
                global schedule
                schedule = sched[i][j]


timezone = 2
offset = tzoffset(None, timezone * 3600)  # offset in seconds


def time_update():
    global now,hour,minute
    now = datetime.now(offset)
    hour = int(now.strftime("%H"))
    minute = int(now.strftime("%M"))


bot = telebot.TeleBot(cfg.TOKEN)


def day_change(arg):
    return arg + count



def hours_para():

    h1 = [[9, 0], [10, 30], [12, 30], [14, 0], [15, 30], [16, 50]]
    h2 = [[10, 20], [11, 50], [13, 50], [15, 20], [16, 50], [17, 0]]

    if hour < h1[0][0]:
        return 0, (h1[0][0] - hour)*60+h1[0][1]-minute

    for i in range(0, 5):
        left = (h2[i][0] - hour)*60+h2[i][1]-minute
        if left >= 0:
            if left >80:
                break
            print('here1')
            return i+1, left
    if (hour == h1[5][0] and minute > h1[4][1]) or (hour >= h2[5][0]):
        return 6, None
    else:
        return None,None


def hours_break():
    h1 = [[10, 20], [11, 50], [13, 50], [15, 20]]
    h2 = [[10, 30], [12, 30], [14, 0], [15, 30]]
    for i in range(0, 4):
        left = (h2[i][0] - hour) * 60 + h2[i][1] - minute
        if left >= 0:
            print('here2')
            return i + 1, left


def week_now(change=0):
    week = (int(now.strftime("%V")) + change) % 2
    # Учебный год начинаться с четной недели (не совпадает)
    if week == 1:
        return schedule[1]
    elif week == 0:
        return schedule[0]


def number_of_para(arg):
    return (week_now().get(now.weekday())).get(arg)


def para_today_by_arg(key=0):

    para_numb, left = hours_para()
    print(para_numb)
    if para_numb is not None:
        numb = key + para_numb
    else:
        break_numb, left = hours_break()
        if key == 0:
            return "Сейчас перемена после пары №" + str(break_numb) + "\nДо следующей пары осталось: " + str(left) + \
                   " минут"
        elif key > 0:
            numb = break_numb + key
        else:
            numb = break_numb + key + 1
    if numb <= 0:
        return "Пары ещё не начались" + "\nДо первой пары: "+str(left) + " минут"
    elif numb <= 5:
        para = number_of_para(numb)
        if para is not None:
            return "\n\t*" + dots +"Пара №" + str(numb) + dots + "*\n\n*У первой подгруппы:*\n" + para[0] + "\n\n*У второй подгруппы:*\n" + para[1] + \
                   "\nДо конца пары: " + str(left) + " минут"
        else:
            return "\nУ первой и второй подгруппы сейчас нет пар"
    elif numb >= 6:
        return "Пары уже закончились"


def para_today_by_number(numb):
    para = number_of_para(numb)
    return "\nПара №" + str(numb) + "\nУ первой подгруппы: " + para[0] + "\nУ второй подгруппы: " + para[1]


def para_by_key_word(day):
    if now.weekday() > day >= 0:
        another_week = 1
        day = day_change(day)
    else:
        day = day_change(day)
        another_week = day // 7

    def output(numb, key=0):
        return "\n\t*" + dots +str(numb) + " пара" + dots + "*\n" + "\n*Подгруппа А:*\n" + \
               (week_now(another_week).get(key % 7)).get(numb)[0] + "\n\n*Подгруппа В:*\n" + \
               (week_now(another_week).get(key % 7)).get(numb)[1] + "\n\n"

    out = "\n"
    for i in range(1, 6):
        out += output(i, day)
    return out


chatId = None



def checkAddNewGroup(chat_id, id_input):
    for i in group:
        for j in group[i]:
            if str(j) == str(id_input):
                with open("chatid.txt", "a", encoding="utf8") as f:
                    f.write("{chat_id}:{id_input}\n".format(chat_id=str(chat_id), id_input=str(id_input)))
                return 1
    return 0


def checkChatId(chat_id):
    with open("chatid.txt", "r", encoding="utf8") as f:
        for line in f:
            if str(chat_id) in line:

                grp = line.split(":")[1]
                grp = grp.replace("\n", "")
                return str(grp)
    return 0

def checkReplaceOldGroup(chat_id, id_input):

    for i in group:
        for j in group[i]:
            if str(j) == str(id_input):
                with open("chatid.txt", "r", encoding="utf8") as f:
                    id_list = f.readlines()
                    amountOfLines = range(len(id_list))
                    for i in amountOfLines:
                        grp = id_list[i].split(":")
                        if str(chat_id) == grp[0]:
                            changed = [chat_id, id_input]
                            changedIndex = i

                            writeToFile = ""
                            for l in amountOfLines:
                                if l != changedIndex:
                                    writeToFile += id_list[l].split(":")[0]+str(":")+id_list[l].split(":")[1]
                                else:
                                    writeToFile += str(changed[0])+str(":")+str(changed[1])+"\n"
                            with open("chatid.txt","w",encoding="utf8") as f:
                                f.write(writeToFile)
                            return str(id_input)
    return 0





@bot.message_handler(commands=['help', 'start', 'para'])
def first(message):
    first_buttons = telebot.types.ReplyKeyboardMarkup(True, True)
    first_buttons.row('Какая сейчас пара?', 'Какая следующая пара')
    first_buttons.row('Какие пары сегодня?', 'Какие пары завтра?')
    bot.send_message(message.chat.id, 'Что Вы хотите узнать?', reply_markup=first_buttons)




def listener(message):
    time_update()

    msg_txt = ""
    chat_id = ""

    for m in message:
        chat_id = m.chat.id

        if m.content_type == 'text':
            msg_txt = m.text.lower()


    def the_day(value):
        return (now.weekday() + value) % 7

    msg_txt = msg_txt.replace('?', '')
    msg_txt = msg_txt.replace('!', '')

    split_msg = msg_txt.split()


    for i in ['пара', 'пары', 'расписание']:
        for j in split_msg:
            if i == j:

                grp = checkChatId(chat_id)

                for k in split_msg:
                    if k == 'группа':
                        if grp == 0:
                            for g in split_msg:
                                if checkAddNewGroup(chat_id, g) == 1:
                                    bot.send_message(chat_id, 'Успех')
                                    print("Успех")
                                    break
                            else:
                                bot.send_message(chat_id, 'Провал')
                                print("Провал")
                        else:
                            result = 0
                            for g in split_msg:
                                result = checkReplaceOldGroup(chat_id, g)
                                if result != 0:
                                    bot.send_message(chat_id, 'Группа успешно изменена на {}'.format(result))
                                    break
                            if result == 0:
                                bot.send_message(chat_id, 'Неверно указана группа или другая ошибка')


                grp = checkChatId(chat_id)

                if grp == 0:
                    bot.send_message(chat_id, 'Чата id{} нет в базе.\nУкажите вашу группу написав: \n"расписание группа [номер группы]"'.format(chat_id))

                else:
                    chooseSched(grp)

                    msg_txt = msg_txt.replace(i, '')
                    global count
                    count = msg_txt.count('после') - msg_txt.count('поза') - msg_txt.count('перед') - msg_txt.count('до')

                    msg_txt = (msg_txt.strip())
                    msg_txt += " "
                    print(msg_txt)

                    def check():
                        i=-1
                        while i<12:
                            for slovo in arg[i]:
                                if slovo in msg_txt:

                                    if i <= 1:
                                        return para_by_key_word(the_day(i))
                                    elif i <= 8:
                                        return para_by_key_word(i-2)
                                    elif i == 9:
                                        return para_today_by_number(int(slovo))
                                    elif i <= 11:
                                        return para_today_by_arg(i-10)
                            i += 1
                        else:
                            return 0

                    send = check()

                    if send != 0:
                        bot.send_message(chat_id, "`альфа тест`\n" + str(send), parse_mode= 'Markdown')
                    break


bot.set_update_listener(listener)

try:
    bot.polling(none_stop=True)
except:
    pass
