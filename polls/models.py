from django.db import models
from django.contrib.auth import get_user_model
import datetime


class Poll(models.Model):  # модель опроса
    title = models.CharField()  # название
    start_date = models.DateField()  # дата старта
    end_date = models.DateField()  # дата окончания
    desc = models.TextField()  # описание


class Question(models.Model):  # модель вопроса
    TEXT = 'TEXT'
    CHOICE = 'CHOICE'
    MULTI = 'MULTI'
    QUESTION_TYPE = [
        (TEXT, 'Текст'),
        (CHOICE, 'Выбор одного варианта'),
        (MULTI, 'Выбор нескольких вариантов')

    ]

    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    text = models.CharField()
    type = models.CharField(
        max_length=6,
        choices=QUESTION_TYPE,
        default=TEXT,
    )