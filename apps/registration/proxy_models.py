from .mixins import ProxyModelReportMixin, ReportManager
from .models import Intern


class InternProxy(ProxyModelReportMixin, Intern):
    class Meta:
        proxy = True

    proxy_objects = ReportManager()

    def report_intern_full_name(self):
        return self.full_name

    report_intern_full_name.verbose_name = 'full_name'

    def report_intern_address(self):
        return self.address

    report_intern_address.verbose_name = 'address'

    def report_intern_phone_number(self):
        return self.contact_info

    report_intern_phone_number.verbose_name = 'contact_info'

    def report_intern_email(self):
        return self.email

    report_intern_email.verbose_name = 'email'

    def report_intern_position(self):
        return self.position

    report_intern_position.verbose_name = 'position'

    def report_intern_start_date(self):
        return self.internship_start.strftime('%d.%m.%Y') if self.internship_start else 'Не указано'

    report_intern_start_date.verbose_name = 'internship_start'

    def report_intern_end_date(self):
        return self.internship_end.strftime('%d.%m.%Y') if self.internship_end else 'Не указано'

    report_intern_end_date.verbose_name = 'internship_end'

    def report_intern_report_date(self):
        return self.date_of_issue.strftime('%d.%m.%Y')

    report_intern_report_date.verbose_name = 'date_of_issue'

    def report_intern_report_created_at(self):
        return self.created_at.strftime('%d.%m.%Y %H:%M') if self.created_at else 'Не указано'

    report_intern_report_created_at.verbose_name = 'created_at'

    def report_intern_report_app_number(self):
        return self.application_number

    report_intern_report_app_number.verbose_name = 'app_number'

    def report_intern_report_id(self):
        return self.ID_doc,

    report_intern_report_id.verbose_name = 'ID'

    def report_intern_report_inn(self):
        return self.INN

    report_intern_report_inn.verbose_name = 'INN'

    def report_intern_report_authority(self):
        return self.authority

    report_intern_report_authority.verbose_name = 'authority'

    def report_intern_is_application_signed(self):
        return self.is_application_signed

    report_intern_is_application_signed.verbose_name = "is_application_signed"
