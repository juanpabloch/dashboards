from base import models


def is_staff(request):
    user = request.user
    if user.is_staff:
        return True
    else:
        user_db = models.User.objects.filter(id=user.id).first()
        return True if user_db and user_db.is_staff else False


def is_superuser(request):
    user = request.user
    if user.is_superuser:
        return True
    else:
        user_db = models.User.objects.filter(id=user.id).first()
        return True if user_db and user_db.is_superuser else False
