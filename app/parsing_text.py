from cmath import phase
from datetime import datetime, timedelta
from app.google_sheets import fill_data_sheets
from config import validate_config

EXPENSES = {"выплата": "Выплата", "подписки": "Подписки", "коннекты": "Коннекты", "расходы": "Другие расходы"}
INCOMES = {"upwork": "UpWork", "клиент": "Оплата от клиента", "доходы": "Другие доходы"}
TIME_DICT = {
    "сегодня": datetime.now(),
    "вчера": datetime.now() - timedelta(days=1),
    "завтра": datetime.now() + timedelta(days=1)
}

def validate_input(phrase: list) -> bool:
    if not phase:
        raise ValueError("Пустая строка недопустима")
    elif len(phrase) < 3:
        raise ValueError("Фраза слишком короткая. Ожидается минимум <дата><тип><сумма>")



def parse_time(date: str) -> str | datetime:
    if date.lower() in TIME_DICT:
        return TIME_DICT[date.lower()].strftime("%Y-%m-%d")
    else:
        try:
            parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
            return str(parsed_date)
        except ValueError:
            raise ValueError("Введенной даты не существует или она введена не правильно")


def determine_category(word: str):
    lower_word = word.lower()
    if lower_word in INCOMES:
        return INCOMES[lower_word], True
    elif lower_word in EXPENSES:
        return EXPENSES[lower_word], False
    else:
        raise ValueError(f"Неизвестный тип операции: '{word}'. Доступные типы: {list(INCOMES.keys()) + list(EXPENSES.keys())}")


def parse_amount(bal: str) -> int:
    try:
        return int(bal)
    except ValueError:
        raise ValueError(f"Сумма '{bal}' не является целым числом.")



def process_phrase(phrase: str):

    validate_config()

    phrase_words = phrase.split(" ")

    validate_input(phrase_words)

    date_part = parse_time(phrase_words[0])
    category_part = determine_category(phrase_words[1])
    description_part = " ".join(phrase_words[2:-1])
    amount_part = parse_amount(phrase_words[-1])

    data_to_sheet = [date_part, category_part[0], description_part, amount_part]
    check_change = category_part[1]

    fill_data_sheets(data_to_sheet, check_change)

    return data_to_sheet


