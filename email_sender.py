import logging

def send_cold_email(target_email, subject, body):
    logging.info(f"تم محاكاة إرسال الإيميل إلى {target_email} بنجاح!")
    return True
