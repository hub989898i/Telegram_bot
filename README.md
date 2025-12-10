# Telegram_bot
Downloader
# Telegram Video Download Bot

ربات تلگرام برای دانلود و ارسال ویدیو از لینک مستقیم

## 🚀 استقرار روی Render

### 1. فورک کردن ریپو
- روی دکمه Fork در GitHub کلیک کنید

### 2. ایجاد سرویس در Render
1. به [render.com](https://render.com) وارد شوید
2. روی "New +" کلیک کنید
3. "Background Worker" را انتخاب کنید
4. ریپو خود را connect کنید

### 3. تنظیمات
- **Name:** telegram-video-bot
- **Environment:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python bot.py`

### 4. متغیرهای محیطی
- `BOT_TOKEN`: توکن ربات از @BotFather
- `ADMIN_ID`: آیدی عددی شما از @userinfobot

### 5. کلیک روی "Create Worker"

## 🔧 اجرای محلی
```bash
# کلون کردن
git clone https://github.com/yourusername/telegram-video-bot.git
cd telegram-video-bot

# نصب وابستگی‌ها
pip install -r requirements.txt

# تنظیم متغیرها
cp .env.example .env
# سپس .env را ویرایش کنید

# اجرای ربات
python bot.py
