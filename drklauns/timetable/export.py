import datetime
import pytz
import xlwt
from io import BytesIO

from django.conf import settings
from slugify import slugify

from drklauns.timetable.models import Summary, Work

riga_tz = pytz.timezone(settings.TIME_ZONE)


def monthly_excel(year: int, month: int):
    output = BytesIO()

    items = Summary.objects.filter(date=datetime.date(year, month, 1)).order_by('employee__first_name', 'employee__last_name', )

    wbk = xlwt.Workbook()

    sheet = wbk.add_sheet("Kopsavilkums %s-%s" % (year, month))
    sheet.write(0, 0, "Kopsavilkums par %s - %s" % (year, month))
    row = 1
    header_row = (
        '#', 'ID', 'Vārds', 'Uzvārds', 'Pers.kods', 'Līguma NR', 'Likme', 'Stundas', 'Alga', 'Procedūru skaits', 'Kontaktu skaits')

    for col, value in enumerate(header_row):
        sheet.write(row, col, value)
    row = 2
    for index, item in enumerate(items, start=1):
        salary = round(float(item.employee.contract_rate) * item.hours_worked, 2)
        row_values = (
            index, item.employee_id, item.employee.first_name, item.employee.last_name, item.employee.ssn, item.employee.contract_no, item.employee.contract_rate,
            item.hours_worked, salary, item.total_procedures, item.total_contacts,)

        for col, value in enumerate(row_values):
            sheet.write(row, col, value)
        row += 1

    for item in items:
        sheet = wbk.add_sheet(slugify(str(item)))
        sheet.write(0, 0, "Darbinieka %s visi darbi par %s - %s" % (item.employee, year, month))
        row = 1
        header_row = ('#', 'ID', 'No', 'Līdz', 'Stundu skaits', 'Slimnīca', 'Nodaļa', 'Procedūru skaits', 'Kontaktu skaits', 'Komentāri', 'Pievienots')
        for col, value in enumerate(header_row):
            sheet.write(row, col, value)
        works = Work.objects.filter(employee=item.employee, start__year=item.date.year, start__month=item.date.month)
        row = 2
        for index, work in enumerate(works, start=1):
            row_values = (
                index, work.id, work.start.astimezone(riga_tz).strftime("%Y-%m-%d %H:%M"), work.end.astimezone(riga_tz).strftime("%Y-%m-%d %H:%M"), work.hours_worked, work.department.hospital.name, work.department.name,
                work.number_of_procedures, work.number_of_contacts, work.comments, work.created.astimezone(riga_tz).strftime("%Y-%m-%d %H:%M"))

            for col, value in enumerate(row_values):
                sheet.write(row, col, value)
            row += 1

    wbk.save(output)
    return output
