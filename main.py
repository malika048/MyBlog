# Импорт необходимых для работы модулей
from website import create_app 
import os
from dotenv import load_dotenv


# Создание приложения
app = create_app()
# Загрузка переменных окружения
load_dotenv()


if __name__ == '__main__': # Запуск сервера
    # port = int(os.getenv("PORT"))
    # app.run(port=port, debug=True)
    app.run(debug=True)
