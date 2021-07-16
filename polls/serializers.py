import datetime

from rest_framework import serializers

from .models import Poll, Question, Choice, Answer, Survey

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers


class PKRField(serializers.PrimaryKeyRelatedField):

    def to_internal_value(self, data):
        value = self.get_queryset().get(pk=data)
        return value.id


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ('id', 'text')
        read_only_fields = ('id', )


class QuestionSerializer(serializers.ModelSerializer):

    type = serializers.ChoiceField(
        choices=Question.QUESTION_TYPE, default=Question.TEXT
    )
    choices = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ('id', 'poll', 'text', 'type', 'choices')
        read_only_fields = ('id', )
        extra_kwargs = {
            'poll': {'write_only': True}
        }

    def create_choices(self, question, choices):
        Choice.objects.bulk_create([
            Choice(question=question, **d) for d in choices
        ])

    def create(self, validated_data):
        choices = validated_data.pop('choices', [])
        question = Question.objects.create(**validated_data)
        self.create_choices(question, choices)
        return question

    def update(self, instance, validated_data):
        choices = validated_data.pop('choices', [])
        instance.choices.all().delete()
        self.create_choices(instance, choices)
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance


class PollSerializer(serializers.ModelSerializer):

    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ('id', 'title', 'start_date',
                  'end_date', 'desc', 'questions')
        read_only_fields = ('id', )

    def validate_start_date(self, value):  # делаем замечание, если хотим поменять дату старта после создания опроса
        if self.instance and self.instance.start_date < value:
            raise serializers.ValidationError(
                "Менять дату старта запрещено!"
            )

        return value


class AnswerSerializer(serializers.ModelSerializer):

    choice = ChoiceSerializer(read_only=True)
    choice_id = PKRField(queryset=Choice.objects.all(), write_only=True)

    question = QuestionSerializer(read_only=True)
    question_id = PKRField(
        queryset=Question.objects.all(), write_only=True)

    class Meta:
        model = Answer
        fields = ('id', 'question_id', 'question',
                  'choice_id', 'choice', 'value')
        read_only_fields = ('id', )


class SurveySerializer(serializers.ModelSerializer):

    answers = AnswerSerializer(many=True)
    poll = PollSerializer(read_only=True)
   
    poll_id = PKRField(
        queryset=Poll.objects.filter(end_date__gte=datetime.date.today()),
        write_only=True
    )

    class Meta:
        model = Survey
        fields = ('id', 'poll_id', 'poll', 'user', 'date', 'answers')
        read_only_fields = ('id', 'user', 'date')

    def create(self, validated_data):
        answers = validated_data.pop('answers', [])
        instance = Survey.objects.create(**validated_data)
        Answer.objects.bulk_create([
            Answer(survey=instance, **a) for a in answers
        ])
        return instance
