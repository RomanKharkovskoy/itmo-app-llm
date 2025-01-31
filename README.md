# ITMO App LLM

## Описание
ITMO App LLM - это проект, разработанный для демонстрации возможностей языковых моделей в приложениях. Этот проект включает в себя различные примеры использования и интеграции языковых моделей в реальных приложениях.

## Установка
Для установки и запуска проекта выполните следующие шаги:

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/RomanKharkovskoy/itmo-app-llm.git
    ```
2. Перейдите в директорию проекта:
    ```bash
    cd itmo-app-llm
    ```
3. Соберите Docker контейнер
    ```bash
    docker compose build
    ```

4. Запустите Docker compose
    ```bash
    docker compose up -d
    ```

## Структура проекта
- `app.py` - основной файл приложения FastAPI
- `tools/` - директория с интсрументами (веб-поиск и парсинг itmo.news)
- `data/` - директория с данными для обучения и тестирования
- `utils/` - директория с дополнительными модулями (парсинг результата генерации в JSON)

## Вклад
Если вы хотите внести вклад в проект, пожалуйста, следуйте этим шагам:

1. Форкните репозиторий
2. Создайте новую ветку (`git checkout -b feature-branch`)
3. Внесите изменения и закоммитьте их (`git commit -am 'Add new feature'`)
4. Запушьте изменения в ветку (`git push origin feature-branch`)
5. Создайте Pull Request

## Контакты
Если у вас есть вопросы или предложения, пожалуйста, свяжитесь со мной: 

- E-mail: [roman.kharkovskoy@yandex.ru](roman.kharkovskoy@yandex.ru)
- Telegram: [@RomanKharkovskoy](https://t.me/RomanKharkovskoy)

