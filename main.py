import requests  # Библиотека для отправки HTTP-запросов
import webbrowser  # Библиотека для открытия ссылок в браузере

def main():
    query = input("Введите поисковый запрос: ")
    try:
        # Формируем URL для API-запроса к Википедии
        api_url = f"https://ru.wikipedia.org/w/api.php?action=query&list=search&utf8=&format=json&srsearch={query}"
        # Отправляем запрос и получаем ответ в формате JSON
        json_response = send_get_request(api_url)
        # Обрабатываем полученные данные
        process_response(json_response)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
# Функция для отправки GET-запроса
def send_get_request(api_url):
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()

# Функция для обработки ответа от API
def process_response(json_response):
    search_results = json_response.get("query", {}).get("search", [])
    if not search_results:
        print("Результаты не найдены.")
        return

    # Выводим список результатов поиска с их номерами
    print("\nРезультаты поиска:")
    for i, result in enumerate(search_results, start=1):
        title = result.get("title", "Без названия")  # Название статьи
        page_id = result.get("pageid", "Нет ID")  # Уникальный id страницы
        print(f"{i}. {title} (pageId: {page_id})")  # Выводим номер, название и ID статьи

    # Запрашиваем у пользователя выбор статьи или выход из программы
    choice = input("\nВведите номер статьи для открытия (или 'exit' для выхода): ")

    if choice.lower() == "exit":
        return

    try:
        choice_index = int(choice) - 1
        if 0 <= choice_index < len(search_results):
            page_id = search_results[choice_index]["pageid"]
            open_browser(f"https://ru.wikipedia.org/w/index.php?curid={page_id}")
        else:
            print("Некорректный номер статьи.")
    except ValueError:
        print("Некорректный ввод.")

# Функция для открытия ссылки в браузере
def open_browser(url):
    webbrowser.open(url)
    print(f"Открыта ссылка: {url}")

# Запускаем главную функцию, если файл запускается напрямую
if __name__ == "__main__":
    main()
