from pydantic import EmailStr

from app.config import settings
from app.tasks.celery_app import celery
from PIL import Image
from pathlib import Path
import smtplib

from app.tasks.email_tempalates import create_booking_confirmation_template


@celery.task
def process_pic(
        path: str,
):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized_1000_500 = im.resize((100, 500))
    im_resized_200_100 = im.resize((200, 100))
    im_resized_1000_500.save(f"app/static/images/im_resized_1000_500{im_path.name}")
    im_resized_200_100.save(f"app/static/images/im_resized_200_100{im_path.name}")


# Раскомментировать при использовании celery вместо BackgroundTasks
# @celery.task
def send_booking_confirmation_email(
        booking: dict,
        email_to: EmailStr
):
    # удалить строчку после отладки
    email_to = settings.SMTP_USER

    msg_content = create_booking_confirmation_template(booking, email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
