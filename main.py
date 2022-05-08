# Импорт необходимых для работы модулей
from website import create_app 
import os
from dotenv import load_dotenv


# Создание приложения
app = create_app()
# Загрузка переменных окружения
load_dotenv()


if __name__ == '__main__': # Запуск сервера
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
