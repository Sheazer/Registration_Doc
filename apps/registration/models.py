from django.core.exceptions import ValidationError
from django.db import models

from .utils import generate_documents


class Intern(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    position = models.CharField(max_length=255, verbose_name="Название позиции")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    email = models.EmailField(verbose_name="Почта")
    contact_info = models.CharField(max_length=255, verbose_name="Контактные данные")
    internship_start = models.DateField(verbose_name="Начало стажировки")
    internship_end = models.DateField(verbose_name="Окончание стажировки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_application_signed = models.BooleanField(default=False, verbose_name="Заявление подписано")
    application_number = models.CharField(max_length=50, unique=True, blank=True, null=True,
                                          verbose_name="Номер заявления")
    ID_doc = models.CharField(max_length=20, verbose_name="Номер документа")
    INN = models.IntegerField(verbose_name="ИНН")
    authority = models.CharField(max_length=255, verbose_name="Орган выдачи")
    date_of_issue = models.DateField(verbose_name="Дата выдачи")

    def clean(self):
        # 1. Проверка, что дата окончания стажировки позже даты начала
        if self.internship_end < self.internship_start:
            raise ValidationError({"internship_end": "Дата окончания стажировки должна быть позже даты начала."})

        # 2. Проверка, что ИНН состоит из 12 цифр
        if not (100000000000 <= self.INN <= 999999999999):
            raise ValidationError({"INN": "ИНН должен содержать 12 цифр."})

        # 3. Проверка, что email содержит "@" и "."
        if "@" not in self.email or "." not in self.email.split("@")[-1]:
            raise ValidationError({"email": "Некорректный email."})

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Стажер'
        verbose_name_plural = 'Стажеры'

    def save(self, *args, **kwargs):
        try:
            generate_documents(self)
        except Exception as e:
            raise ValidationError(f"Ошибка при генерации документов: {str(e)}")
        super().save(*args, **kwargs)
