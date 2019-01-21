from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from datetime import datetime

import xlwt

from . import models


def int_to_Roman(num):
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    syb = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
    ]
    roman_num = ''
    i = 0
    while  num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num


class CreateMessage(generic.CreateView):
    fields = ("name", "dep", "div")
    model = models.Message
    success_url = reverse_lazy('departments:success_message')
    

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            depart = models.Department.objects.get(name__iexact=form.cleaned_data['dep'])
        except models.Department.DoesNotExist:
            depart = models.Department.objects.create(name=form.cleaned_data['dep'])
            try:
                models.Division.objects.get(name__iexact=form.cleaned_data['div'], department_id=depart.pk)
            except models.Division.DoesNotExist:
                models.Division.objects.create(name=form.cleaned_data['div'], department=depart)
        else:
            try:
                models.Division.objects.get(name__iexact=form.cleaned_data['div'],
                                            department__name__iexact=form.cleaned_data['dep'])
            except models.Division.DoesNotExist:
                models.Division.objects.create(name=form.cleaned_data['div'], department=depart)
        division = models.Division.objects.get(name__iexact=form.cleaned_data['div'], 
                                               department__name__iexact=form.cleaned_data['dep'])
        no = division.message_set.all().count() + 1
        self.object.nomor = "{0:03d}/{1}-{2}/{3}/{4}".format(no,
            form.cleaned_data['dep'],
            form.cleaned_data['div'],
            int_to_Roman(datetime.now().month),
            datetime.now().year)
        self.object.division = division
        self.object.save()    
        return super().form_valid(form)
        

class SuccessMessage(generic.TemplateView):
    template_name = 'departments/success_message.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = models.Message.objects.latest('id')
        return context


def some_view(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = "attachment; filename=messages.xls"
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Messages')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Nomor Surat', 'Departemen', 'Divisi', 'Nama Pengirim',]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = models.Message.objects.all().values_list('nomor', 'dep', 'div', 'name')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response