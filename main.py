import requests
import json
import time
import logging

BOT_TOKEN = "6714968662:AAE2QLLUIM5AMrmEvA43YMqZTn2LayvDJSs"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

logging.basicConfig(filename = 'bot_logs.txt', level = logging.INFO, format = '%(asctime)s - %(message)s')

MAIN_KEYBOARD = {
	"keyboard": [
		["Рецепты", "Советы"],
		["Мотивация"]
	],
	"resize_keyboard": True
}

RECIPES_KEYBOARD = {
	"keyboard": [
		["Завтрак", "Обед"],
		["Ужин", "Перекус"]
	],
	"resize_keyboard": True
}

TIPS_KEYBOARD = {
	"keyboard": [
		["Личная жизнь", "Работа"],
		["Учёба", "Спорт"]
	],
	"resize_keyboard": True
}


def send_message(chat_id, text, reply_markup = None):
	params = {
		"chat_id": chat_id,
		"text": text,
		"parse_mode": "Markdown",
	}

	if reply_markup:
		params["reply_markup"] = json.dumps(reply_markup)

	response = requests.post(f"{TELEGRAM_API_URL}/sendMessage", params = params)
	return response.json()


def handle_start(chat_id):
	text = "Привет! Я бот с различными функциями. Выбери категорию:"
	send_message(chat_id, text, reply_markup = MAIN_KEYBOARD)


def handle_continue(chat_id):
	text = "Выбери новую категорию:"
	send_message(chat_id, text, reply_markup = MAIN_KEYBOARD)


def handle_category(chat_id, category):
	if category == "Рецепты":
		text = "Выбери подкатегорию:"
		send_message(chat_id, text, reply_markup = RECIPES_KEYBOARD)
	elif category == "Советы":
		text = "Выбери подкатегорию:"
		send_message(chat_id, text, reply_markup = TIPS_KEYBOARD)
	elif category == "Мотивация":
		text = "Мотивацию нужно поднять!"
		send_message(chat_id, text)
		handle_continue(chat_id)


def handle_recipes(chat_id, subcategory):
	recipes_dict = {
		"Завтрак": """
        Омлет с овощами:
        - Яйца - 3 шт.
        - Помидоры - 1 шт.
        - Лук - 1 шт.
        - Перец - 1 шт.
        - Соль, перец - по вкусу
        - Разогреть сковороду, добавить масло.
        - Нарезать овощи и обжаривать их.
        - Взбить яйца, добавить в сковороду.
        - Тщательно перемешивать, пока не приготовится.
        - Подавать горячим с зеленью.
    """,

		"Обед": """
        Паста с томатным соусом и говядиной:
        - Паста - 200 г.
        - Говядина - 200 г.
        - Лук - 1 шт.
        - Чеснок - 2 зубчика
        - Томатный соус - 400 г.
        - Специи - по вкусу
        - Обжарить лук и чеснок.
        - Добавить мелко нарезанную говядину, обжаривать.
        - Добавить томатный соус и специи.
        - Варить пасту, смешать с соусом.
        - Подавать горячим.
    """,

		"Ужин": """
        Курица с картошкой в духовке:
        - Курица - 1 шт.
        - Картошка - 4 шт.
        - Лук - 1 шт.
        - Чеснок - 3 зубчика
        - Розмарин, тимьян - по вкусу
        - Соль, перец - по вкусу
        - Нарезать курицу и картошку.
        - Обжарить лук и чеснок.
        - Смешать все ингредиенты в форме для запекания.
        - Посыпать специями, запечь в духовке.
        - Подавать горячим.
    """,

		"Перекус": """
        Фруктовый салат:
        - Яблоко - 1 шт.
        - Груша - 1 шт.
        - Банан - 1 шт.
        - Киви - 2 шт.
        - Мед - 2 ложки
        - Орехи - 50 г.
        - Нарезать фрукты, перемешать.
        - Полить медом, посыпать орехами.
        - Подавать в холодном виде.
    """
	}

	text = f"Рецепт на {subcategory}:\n {recipes_dict.get(subcategory, 'Рецепт не найден.')}"
	send_message(chat_id, text)
	handle_continue(chat_id)


def handle_tips(chat_id, subcategory):
	tips_dict = {
		"Личная жизнь": """
        Совет по личной жизни: Не забывайте выделять время для себя и близких.
        Важно находить баланс между работой и личной жизнью.
    """,

		"Работа": """
        Совет по работе: Установите ясные цели и приоритеты для повышения эффективности.
        Регулярно делайте перерывы, чтобы сохранить продуктивность и избежать усталости.
    """,

		"Учёба": """
        Совет по учебе: Планируйте свое время и ставьте конкретные цели.
        Используйте различные методы обучения для лучшего усвоения материала.
    """,

		"Спорт": """
        Совет по спорту: Регулярно занимайтесь физической активностью для поддержания здоровья.
        Найдите вид спорта, который приносит вам удовольствие, чтобы поддерживать мотивацию.
    """
	}

	text = f"Совет для категории {subcategory}:\n {tips_dict.get(subcategory, 'Совет не найден.')}"
	send_message(chat_id, text)
	handle_continue(chat_id)


def handle_message(update):
	chat_id = update["message"]["chat"]["id"]
	text = update["message"]["text"]

	if text == "/start":
		handle_start(chat_id)
	elif text in ["Рецепты", "Советы", "Мотивация", "Полезные подборки"]:
		handle_category(chat_id, text)
	elif text in ["Завтрак", "Обед", "Ужин", "Перекус"]:
		handle_recipes(chat_id, text)
	elif text in ["Личная жизнь", "Работа", "Учёба", "Спорт"]:
		handle_tips(chat_id, text)


def main():
	offset = None

	while True:
		try:
			params = {"offset": offset, "timeout": 30}
			response = requests.get(f"{TELEGRAM_API_URL}/getUpdates", params = params)
			data = response.json()

			if "result" in data and data["result"]:
				for update in data["result"]:
					offset = update["update_id"] + 1
					if "message" in update:
						handle_message(update)
			else:
				print("No updates")

			time.sleep(1)
		except Exception as e:
			print(f"Error: {e}")


if __name__ == "__main__":
	main()
