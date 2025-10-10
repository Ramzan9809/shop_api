import datetime
from rest_framework.exceptions import PermissionDenied

def validate_user_age_from_token(request):
   
    user = getattr(request, "user", None)

    if not user or not hasattr(user, "birthdate") or not user.birthdate:
        raise PermissionDenied("Укажите дату рождения, чтобы создать продукт.")

    today = datetime.date.today()
    birthdate = user.birthdate
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

    if age < 18:
        raise PermissionDenied("Вам должно быть 18 лет, чтобы создать продукт.")

    return True
