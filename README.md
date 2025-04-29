Возможности:
- Загрузка файлов `.txt` и `.pdf` (максимум 5MB)
- Обработка текста в кодировке UTF-8
- Расчёт TF и IDF по всем загруженным документам
- Сортировка по убыванию IDF
- Пагинация результатов
- Безопасная работа с пользовательскими файлами

Запуск:
- python -m venv venv
- source venv/bin/activate
- Для Windows: venv\Scripts\activate
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py runserver
