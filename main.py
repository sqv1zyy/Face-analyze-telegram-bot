
from deepface import DeepFace
import telebot
import json
import time
import os


bot = telebot.TeleBot("", parse_mode=None) # в кавычках указываем Api ключ бота
images = dict()


@bot.message_handler(commands=['start', 'help', 'начать', 'меню'])
def start(message):
    bot.send_message(message.from_user.id,
                     "Привет, я алгоритм для анализа фотографий\n/analyze")


@bot.message_handler(commands=['analyze'])
def a(message):
    if message.text == '/analyze':
        bot.send_message(message.from_user.id, 'Отправьте фото для анализа')
        bot.register_next_step_handler(message, handle_docs_photo2)


def clear_content(chat_id):
    try:
        for img in images[chat_id]:
            os.remove(img)
    except Exception as e:
        time.sleep(3)
        clear_content(chat_id)
    images[chat_id] = []


@bot.message_handler(content_types=['photo'])
def handle_docs_photo2(message):
    print(message.photo[:-1])
    images[str(message.chat.id)] = []
    try:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)

        downloaded_file = bot.download_file(file_info.file_path)

        src = 'tmp/' + file_info.file_path

        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "Фото добавлено")
        images[str(message.chat.id)].append(src)
        result_dict = DeepFace.analyze(img_path=src, actions=['age', 'gender', 'race', 'emotion'])

        with open('face_analyze.json', 'w') as file:
            json.dump(result_dict, file, indent=4, ensure_ascii=False)
        f = open('face_analyze.json')
        bot.send_document(message.chat.id, f)
    except Exception as e:
        bot.reply_to(message, e)
    time.sleep(5)
    if 0 == 0:
        clear_content(str(message.chat.id))


bot.polling(none_stop=True, interval=0)