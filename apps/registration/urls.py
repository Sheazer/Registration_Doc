from django.urls import path
from .views import download_intern_document, download_nda_document

urlpatterns = [
    path('download_nda/<int:intern_id>/', download_nda_document, name='download_nda'),
    path('download_intern_document/<int:intern_id>/', download_intern_document, name='download_intern_document'),
]