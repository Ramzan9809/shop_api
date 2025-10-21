from celery import shared_task
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from users.models import VerificationCode
from django.utils import timezone
import time


@shared_task
def generate_verification_code():
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    verification_code = VerificationCode.objects.create(code=code)
    print(f"Генерация кода: {code}")
    return code


@shared_task
def delete_old_verification_codes():
    thirty_days_ago = timezone.now() - timezone.timedelta(days=5)
    old_codes = VerificationCode.objects.filter(created_at__lt=thirty_days_ago)
    deleted_count, _ = old_codes.delete()
    print(f"Удалено {deleted_count} старых записей.")
    return f"Удалено {deleted_count} старых записей."


@shared_task
def send_daily_report_email():
    subject = "Ежедневный отчет"
    message = "Вот ваш ежедневный отчет!"
    recipient_list = ['ramzan.rgwctx9809@gmail.com']
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        fail_silently=False,
    )
    
    print("Ежедневный отчет отправлен!")
    return "OK"
