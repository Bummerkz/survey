from django.db import models
from django.contrib.auth import get_user_model
import datetime


class Poll(models.Model):  # модель опроса
    title = models.CharField(max_length=200)  # название
    start_date = models.DateField()  # дата старта
    end_date = models.DateField()  # дата окончания
    desc = models.TextField()  # описание


class Question(models.Model):  # модель вопроса
    
    # типы ответов
    TEXT = 'TEXT'
    CHOICE = 'CHOICE'
    MULTI = 'MULTI'
    
    QUESTION_TYPE = [
        (TEXT, 'Текст'),
        (CHOICE, 'Выбор одного варианта'),
        (MULTI, 'Выбор нескольких вариантов')

    ]

    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)  # ссылка на опрос
    text = models.CharField(max_length=1000)  # текст вопроса
    type = models.CharField(
        max_length=6,
        choices=QUESTION_TYPE,
        default=TEXT,
    )  # тип принимаемого ответа


class Survey(models.Model):  # модель активных опросов
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)  # ссылка на опрос
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)  # пользоватиель
    date = models.DateField(default=datetime.date.today(), editable=False)  # дата прохождения


class Choice(models.Model):  # модель выборат ответа
    question = models.ForeignKey(
        'Question', related_name='choices', on_delete=models.CASCADE
    )  # ссылка на вопрос
    text = models.CharField(max_length=200, default='')  # текст выбора  


class Answer(models.Model):  # модель ответа
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # ссылка на вопрос
    survey = models.ForeignKey(Survey, related_name='answers', on_delete=models.CASCADE)  # ссылка на активный опрос
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)  # ссылка на выбор ответа
    value = models.CharField(max_length=128, blank=True, null=True)  # ответ