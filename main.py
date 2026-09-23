import time
import logging
from ai import generate_email
from email_sender import send_cold_email

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def process_leads(leads_list):
    total = len(leads_list)
    logging.info(f"بدء الحملة... جاري معالجة {total} عملاء.")
    print("=" * 40)

    for index, lead in enumerate(leads_list, 1):
        name = lead.get("name")
        email = lead.get("email")
        industry = lead.get("industry")
        pain = lead.get("pain_point")
        
        logging.info(f"[{index}/{total}] جاري العمل على العميل: {name}")
        
        email_data = generate_email(name, industry, pain)
        if not email_data:
            logging.warning(f"تخطي العميل {name} لفشل التوليد.")
            print("-" * 40)
            continue
            
        subject = email_data.get("subject")
        body = email_data.get("body")
        
        success = send_cold_email(email, subject, body)
        if success:
            logging.info(f"تم إرسال الإيميل للعميل '{name}'.")
        else:
            logging.error(f"فشل الإرسال للعميل '{name}'.")
        
        print("-" * 40)
        if index < total:
            time.sleep(3)

if __name__ == "__main__":
    sample_leads = [
        {"name": "شركة القمة", "email": "test1@test.com", "industry": "التسويق", "pain_point": "ضعف المبيعات"},
        {"name": "الأفق", "email": "test2@test.com", "industry": "عقارات", "pain_point": "نقص العملاء"}
    ]
    print("تشغيل المايسترو...")
    process_leads(sample_leads)
