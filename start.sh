#!/bin/bash
cd ~/Hotel360
source venv_new/bin/activate
echo "✅ Виртуальное окружение активировано"
echo "🚀 Запускаю сервер на http://127.0.0.1:8000"
python manage.py runserver
