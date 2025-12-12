FROM python:3.12-slim

WORKDIR /app

# جلوگیری از کش شدن بیهوده و فایل‌های pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# نصب پکیج‌ها
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# کپی کردن کدها
COPY . .

# پورت پیش‌فرض
EXPOSE 8000

# دستور اجرا (فعلاً ران‌سرور، بعداً Gunicorn)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]