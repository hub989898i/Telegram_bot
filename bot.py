import os
import logging
import tempfile
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# تنظیمات
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
PORT = int(os.getenv("PORT", 5000))

# لاگینگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور /start"""
    user_id = update.effective_user.id
    
    if user_id == ADMIN_ID:
        await update.message.reply_text(
            "👑 **سلام ادمین!**\n\n"
            "لینک مستقیم ویدیو (MP4) را ارسال کنید.\n"
            "مثال: https://example.com/video.mp4\n\n"
            "⚠️ حداکثر حجم: 50 مگابایت\n"
            f"🚀 سرور: Render.com"
        )
    else:
        await update.message.reply_text(
            "🤖 **ربات دانلود ویدیو**\n\n"
            "⛔ این ربات فقط برای ادمین قابل استفاده است."
        )

async def handle_video_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دریافت و دانلود ویدیو"""
    user_id = update.effective_user.id
    
    # فقط ادمین
    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ دسترسی ندارید!")
        return
    
    video_url = update.message.text.strip()
    
    # بررسی لینک
    if not video_url.startswith(('http://', 'https://')):
        await update.message.reply_text("❌ لطفاً یک لینک معتبر ارسال کنید!")
        return
    
    status_msg = await update.message.reply_text("⏳ در حال بررسی لینک...")
    
    try:
        # ایجاد فایل موقت
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
            temp_path = tmp.name
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
            'Referer': 'https://www.google.com/'
        }
        
        await status_msg.edit_text("📥 در حال دانلود ویدیو...")
        
        # دانلود با timeout
        response = requests.get(video_url, headers=headers, stream=True, timeout=60)
        response.raise_for_status()
        
        # بررسی حجم
        content_length = response.headers.get('content-length')
        if content_length:
            size_mb = int(content_length) / (1024 * 1024)
            if size_mb > 50:
                await status_msg.edit_text(f"❌ حجم ویدیو ({size_mb:.1f}MB) بیشتر از 50MB است!")
                return
        
        # ذخیره فایل
        with open(temp_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        # ارسال ویدیو
        await status_msg.edit_text("✅ دانلود شد! در حال آپلود...")
        
        with open(temp_path, 'rb') as video_file:
            await update.message.reply_video(
                video=video_file,
                caption=f"🎬 ویدیو دانلود شده\n🔗 از: {video_url[:50]}...",
                supports_streaming=True,
                read_timeout=60,
                write_timeout=60,
                connect_timeout=60,
                pool_timeout=60
            )
        
        await status_msg.delete()
        
    except requests.exceptions.Timeout:
        await status_msg.edit_text("❌ زمان دانلود به پایان رسید!")
    except requests.exceptions.RequestException as e:
        await status_msg.edit_text(f"❌ خطا: {str(e)[:100]}")
    except Exception as e:
        logger.error(f"Error: {e}")
        await status_msg.edit_text("❌ خطای ناشناخته رخ داد!")
    finally:
        # پاک‌سازی فایل موقت
        if 'temp_path' in locals():
            try:
                os.unlink(temp_path)
            except:
                pass

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت خطاها"""
    logger.error(f"Error: {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text("❌ خطایی رخ داد!")

def main():
    """تابع اصلی"""
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN تنظیم نشده!")
        return
    
    logger.info(f"🚀 شروع ربات... آیدی ادمین: {ADMIN_ID}")
    
    # ساخت اپلیکیشن
    app = Application.builder().token(BOT_TOKEN).build()
    
    # اضافه کردن هندلرها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video_link))
    app.add_error_handler(error_handler)
    
    # اجرای ربات
    app.run_polling(
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES
    )

if __name__ == "__main__":
    main()
