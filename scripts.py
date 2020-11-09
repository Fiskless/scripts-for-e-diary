from datacenter.models import Schoolkid
from datacenter.models import Lesson
from datacenter.models import Commendation
from datacenter.models import Chastisement
from datacenter.models import Mark
from django.http import Http404
import random


def fix_marks(schoolkid_name):

    try:
        child = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except Schoolkid.DoesNotExist:
        raise Http404("Wrong schoolkid name")

    bad_marks = Mark.objects.filter(schoolkid=child, points__in=[2, 3])
    for bad_mark in bad_marks:
        bad_mark.points = 5
        bad_mark.save()


def remove_chastisements(schoolkid_name):

    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name, )
    except Schoolkid.DoesNotExist:
        raise Http404("Wrong schoolkid name")

    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(schoolkid_name, lesson, year_of_study, group_letter):
    lessons = Lesson.objects.filter(year_of_study=year_of_study, group_letter=group_letter, subject__title__contains=lesson).order_by('-subject').first()
    child = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    commendation_list=['Молодец!',
                       'Отлично!',
                       'Хорошо!',
                       ' Гораздо лучше, чем я ожидал!',
                       'Ты меня приятно удивил!',
                       'Ты, как всегда, точен!',
                       'Талантливо!','Потрясающе!',
                       'Замечательно!',
                       'Так держать!',
                       'Здорово!',
                       'Я тобой горжусь!',
                       'Ты растешь над собой!']
    commendation_text = random.choice(commendation_list)
    Commendation.objects.create(text=commendation_text, created=lessons.date, schoolkid=child, subject=lessons.subject, teacher=lessons.teacher)

