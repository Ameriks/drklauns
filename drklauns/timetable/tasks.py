import datetime

from django.db.models import Sum

from drklauns.timetable.models import Work, Summary


def recalculate_summary(work_id: int=None, work: Work=None):
    if not work:
        work = Work.objects.get(id=work_id)

    dt = datetime.date(work.start.year, work.start.month, 1)
    summary, created = Summary.objects.get_or_create(employee=work.employee, date=dt, defaults={'rate': work.employee.contract_rate})

    totals = Work.objects.filter(start__year=work.start.year, start__month= work.start.month, employee=work.employee).aggregate(hours_worked=Sum('hours_worked'), number_of_contacts=Sum('number_of_contacts'), number_of_procedures=Sum('number_of_procedures'))

    summary.hours_worked = totals.get('hours_worked')
    summary.total_contacts = totals.get('number_of_contacts')
    summary.total_procedures = totals.get('number_of_procedures')

    summary.income = float(summary.rate) * float(summary.hours_worked)

    summary.save()
