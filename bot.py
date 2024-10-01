import telebot
from config import *
from logic import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Доступные команды:"
                     "/start -- команда для запуска бота."
                     "/help -- команда для просмотра команд."
                     "/show_city -- команда для просмотра одного города."
                     "/add_city -- команда для добавления в свои избранные города."
                     "del_city -- команда для удаления из своих избранных городов."
                    "show_my_cities -- команда которая показывает избранные города"                        )


@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    city_name = message.text.split()[-1]
    # Реализуй отрисовку города по запросу
    user_id = message.chat.id
    manager.create_grapf(path=f'{user_id}.png', cities=[city_name])
    with open(f'{user_id}.png', 'rb')as map:
        bot.send_photo(user_id, map)
        

@bot.message_handler(commands=['del_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    city_name = message.text.split()[-1]
    if manager.del_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно удалён!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['add_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    city_name = message.text.split()[-1]
    if manager.add_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранён!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    cities = manager.select_cities(message.chat.id)
    # Реализуй отрисовку всех городов
    user_id = message.chat.id
    if cities:
        manager.create_grapf(path=f'{user_id}_citeis.png', cities=cities)
        with open(f'{user_id}_citeis.png', 'rb')as map:
            bot.send_photo(user_id, map)



if __name__=="__main__":
    manager = DB_Map(DATABASE)
    bot.polling()
