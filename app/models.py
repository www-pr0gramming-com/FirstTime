from django.db import models

# from django.contrib.auth import get_user_model

# User = get_user_model()

from django.contrib.auth.models import AbstractUser

from django.db.models.signals import (
    pre_save,
    post_save,
    pre_delete,
    post_delete,
)


class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)


class UserProfile(models.Model):
    class Meta:
        verbose_name_plural = "プロファイル"
        verbose_name = "プロファイル"

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


# class Manager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset()

#     def get_age_below_50(self):
#         return self.get_queryset().filter(age__lt=50)


# class BlankManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(category__isnull=True)


class A001(models.Model):
    class Meta:
        verbose_name_plural = "リーズ"
        verbose_name = "リード"

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(
        "Category",
        related_name="a001",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    profile_picture = models.ImageField(
        null=True, blank=True, upload_to="profile_pictures/"
    )

    # objects = Manager()
    # blank_objects = BlankManager()
    # A001.blank_objects.all()

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"


class Agent(models.Model):
    class Meta:
        verbose_name_plural = "エージェント"
        verbose_name = "エージェント"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class Category(models.Model):
    class Meta:
        verbose_name_plural = "カテゴリー"
        verbose_name = "カテゴリー"

    # contact converted unconverted
    name = models.CharField(max_length=30, verbose_name="名前")
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


def post_user_created_signal(sender, instance, created, **kwagrs):
    # print(sender, instance, created, kwagrs)
    if created == True:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)
