from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Intern


@admin.register(Intern)
class InternAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'position', 'download_link', 'download_nda_link')  # Добавляем кастомную колонку
    search_fields = ('full_name', 'email')
    exclude = ("created_at", "application_number")
    readonly_fields = ("created_at",)

    def download_link(self, obj):
        # Генерация ссылки для скачивания документа
        url = reverse('download_intern_document', args=[obj.id])
        return format_html('<a href="{}">Скачать документ</a>', url)
    download_link.short_description = 'Документ'  # Название колонки

    def download_nda_link(self, obj):
        if obj.is_application_signed:
            url = reverse('download_nda', args=[obj.id])
            return format_html('<a href="{}">📄 Скачать NDA</a>', url)
        return "Заявление не подписано"

    download_nda_link.short_description = 'NDA'
