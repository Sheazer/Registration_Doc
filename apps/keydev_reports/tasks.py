from typing import Iterable, Dict, List, Union

from django.db import connection

from celery import shared_task

from .sql_utils import execute_sql_query
from .exporter import TemplateReportExporter, ReportExporter


@shared_task
def get_template_report(
        report_data: Iterable,
        user_name: str,
        report_id: int,
        provider_name: str,
        file_name: str | None = None
):
    """
    Функция для отчетов с шаблонами.
    :param report_data: Данные для отчета.
    :param user_name: Имя пользователя.
    :param report_id: Первичный ключ шаблона (ReportTemplate)
    :param provider_name: Название провайдера.
    :param file_name: Название отчета.
    :return: data
    """
    report = TemplateReportExporter(
        report_data=report_data,
        user_name=user_name,
        report_id=report_id,
        provider_name=provider_name,
        file_name=file_name)
    data = dict()
    try:
        files = [report.get_report(), ]
    except Exception as e:
        data['error'] = str(e)
    else:
        data['files'] = files
    return data


@shared_task
def get_no_template_report(
        report_data: Iterable,
        user_name: str,
        report_name: str,
        extension: str,
        provider_name: str,
        file_name: str | None = None
):
    """
    Функция для генерации отчетов.
    :param report_data: Данные для отчета.
    :param user_name: Имя пользователя.
    :param report_name: Название отчета.
    :param extension: Расширение отчета.
    :param provider_name: Название провайдера.
    :param file_name: Название отчета.
    :return: data
    """
    report = ReportExporter(
        report_data=report_data,
        user_name=user_name,
        report_name=report_name,
        extension=extension,
        provider_name=provider_name,
        file_name=file_name)
    data = dict()
    try:
        files = [report.get_report(), ]
    except Exception as e:
        data['error'] = str(e)
    else:
        data['files'] = files
    return data


def run_sql_functions(
        sql_functions: Union[str, Dict[str, str]],
        func_args: List,
        fields: str = '*'
) -> Union[List[Dict], Dict[str, List[Dict]]]:
    """
    Функция для получения данных из одиночных или множественных SQL-функций.

    :param sql_functions: Sql-функция.
    :param func_args: Аргументы SQL-запроса.
    :param fields: Выбранные поля для запроса.
    :return: Результат выполнения SQL-функций в виде списка словарей или словаря,
    где ключи - имена функций, значения - списки словарей с результатами.
    """
    data = {} if isinstance(sql_functions, dict) else []

    if isinstance(sql_functions, str):
        sql_function = {f'{sql_functions}': sql_functions}
    else:
        sql_function = sql_functions

    with connection.cursor() as cursor:
        for key, func_name in sql_function.items():
            results = execute_sql_query(cursor, func_name, func_args, fields)
            column_names = [column[0] for column in cursor.description]
            if isinstance(data, dict):
                data[key] = results
            else:
                data.extend([dict(zip(column_names, row)) for row in results])

    return data
