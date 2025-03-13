from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Intern
from .utils import generate_documents, generate_nda


def download_intern_document(request, intern_id):
    # Получаем объект Intern
    # intern = get_object_or_404(Intern, id=intern_id)

    # Генерация документа
    response = generate_documents(intern_id)
    return response


def download_nda_document(request, intern_id):
    # Получаем объект Intern
    # intern = get_object_or_404(Intern, id=intern_id)

    # Генерация документа
    response = generate_nda(intern_id)
    return response