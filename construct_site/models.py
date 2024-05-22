from django.db import models
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill
from account.models import UserSite


# Список дополнительных данных
class AdditionalData(models.Model):
    element_id = models.CharField(max_length=40)
    photo = ProcessedImageField(upload_to='images/',
                                null=True, blank=True,
                                processors=[ResizeToFill(240, 240)],
                                format='PNG',
                                options={'quality': 100})
    value = models.TextField(null=True, blank=True)
    user_site = models.ForeignKey(UserSite, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.element_id

    def clean(self):
        if self.value:
            self.value = self.value.strip()


# Поддержка клиентов
class Support(models.Model):
    KIND_CHOICES = (
        (1, "Ватсап"),
        (2, "Номер телефона")
    )
    kind = models.IntegerField(default=1, choices=KIND_CHOICES)
    label = models.CharField(max_length=80, default='Написать по ватсапу')
    user_site = models.ForeignKey(UserSite, on_delete=models.CASCADE)
    bacground_color = models.CharField(max_length=120, default='#25d366')
    text_color = models.CharField(max_length=120, default='#ffffff')
    icon_color = models.CharField(max_length=120, default='#ffffff')
    whatsapp_text = models.CharField(max_length=120, blank=True, null=True, default='')
    is_main = models.BooleanField(default=False)


# Менеджеры
class PhoneNumber(models.Model):
    phone_number = models.CharField(max_length=18, blank=True, null=True)
    support = models.ForeignKey(Support, on_delete=models.CASCADE)
    last_date =  models.DateTimeField(auto_now_add=True, blank=True)


# Часто задаваемые вопросы
class FAQ(models.Model):
    title = models.CharField(max_length=380)
    description = models.TextField()
    user_site = models.ForeignKey(UserSite, on_delete=models.CASCADE)
    sorting = models.IntegerField(default=0)