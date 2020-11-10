from datacenter.models import Schoolkid
from datacenter.models import Lesson
from datacenter.models import Commendation
from datacenter.models import Chastisement
from datacenter.models import Mark
import random


def fix_marks(schoolkid_name):

    try:
        child = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        bad_marks = Mark.objects.filter(schoolkid=child, points__in=[2, 3])
        for bad_mark in bad_marks:
            bad_mark.points = 5
            bad_mark.save()
    except Schoolkid.DoesNotExist:
        print("Wrong schoolkid name")
    except Schoolkid.MultipleObjectsReturned:
        print("Wrong schoolkid name")


def remove_chastisements(schoolkid_name):

    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
        chastisements.delete()
    except Schoolkid.DoesNotExist:
        print("Wrong schoolkid name")
    except Schoolkid.MultipleObjectsReturned:
        print("Wrong schoolkid name")


def create_commendation(schoolkid_name, lesson, year_of_study, group_letter):

    try:
        lessons = Lesson.objects.filter(
            year_of_study=year_of_study,
            group_letter=group_letter,
            subject__title__contains=lesson).order_by('-subject').first()
        child = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        commendation_list = ['Молодец!',
                             'Отлично!',
                             'Хорошо!',
                             ' Гораздо лучше, чем я ожидал!',
                             'Ты меня приятно удивил!',
                             'Ты, как всегда, точен!',
                             'Талантливо!',
                             'Потрясающе!',
                             'Замечательно!',
                             'Так держать!',
                             'Здорово!',
                             'Я тобой горжусь!',
                             'Ты растешь над собой!']
        commendation_text = random.choice(commendation_list)
        Commendation.objects.create(text=commendation_text,
                                    created=lessons.date,
                                    schoolkid=child,
                                    subject=lessons.subject,
                                    teacher=lessons.teacher)
    except Schoolkid.DoesNotExist:
        print("Wrong schoolkid name")
    except Schoolkid.MultipleObjectsReturned:
        print("Wrong schoolkid name")
    except AttributeError:
        print("Wrong year of study, group letter or subject title")
