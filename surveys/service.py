from rest_framework import serializers

from .models import Question, AnswerChoice, CompletedSurvey, Answer


def get_answer_choices(validated_data: dict):
    """Tries to get answer choices
    from validated_data. If KeyError occures,
    raises validation error. Else returns answer choices.
    """
    try:
        answer_choices = validated_data.pop('choices')
    except KeyError:
        if validated_data.get('question_type') != 1:
            raise serializers.ValidationError("You must supply 'choices' for all the questions which type isn't equal to 1")
    else:
        return answer_choices


def create_answer_choices(question, answer_choices):
    """If passed question's type isn't 
    equal to 1 (text answer), creates 
    answer choices from passed data.
    """
    if question.question_type != 1:
        for choice in answer_choices:
            AnswerChoice.objects.create(**choice, question=question)


def create_question(validated_data: dict, **kwargs):
    """Creates a new Question's 
    instance from passed data.

    """
    answer_choices = get_answer_choices(validated_data)
    question = Question.objects.create(**validated_data, **kwargs)
    create_answer_choices(question, answer_choices)
    return question


def instance_exists(model, **kwargs) -> tuple:
    """Checks if instance of the passed model 
    with passed keyword args exists. Returns a tuple
    of 2 items: bool exists and instance of the model.
    """
    qs = model.objects.filter(**kwargs)
    if qs.exists():
        return True, qs[0]
    return False, None


def delete_not_updated_instances(queryset, updated_instances_pks: list):
    """Loops throw the queryset and deletes 
    instances whose pk isn't represented in 
    'updated_instances_pks' list.
    """
    for instance in queryset: 
        if instance.pk not in updated_instances_pks:
            instance.delete()


def update_question(question, validated_data):
    """Performs updating of the given 
    question's fields.
    """
    # update question
    question.survey = validated_data.get('survey', question.survey)
    question.text = validated_data.get('text', question.text)
    question.question_type = validated_data.get('question_type', question.question_type) 
    question.save()

    # update question's choices
    if question.question_type != 1:
        updated_answer_choices_pks = list()
        answer_choices = get_answer_choices(validated_data)
        for answer_choice_data in answer_choices:
            if "pk" in answer_choice_data.keys():
                exists, answer_choice = instance_exists(AnswerChoice, pk=answer_choice_data.get("pk"))
                if exists:
                    answer_choice.question = question
                    answer_choice.text = answer_choice_data.get('text', answer_choice.text)
                    answer_choice.save()
                    updated_answer_choices_pks.append(answer_choice.pk)                    
            else: # create answer option if 'pk' wan't supplied
                answer_choice = AnswerChoice.objects.create(**answer_choice_data, question=question)
                updated_answer_choices_pks.append(answer_choice.pk)
        delete_not_updated_instances(question.choices.all(), updated_answer_choices_pks)
    else:
        question.choices.all().delete()

    return question


def update_survey(instance, validated_data):
    """Updates survey instance.
    """
    # update survey
    instance.name = validated_data.get('name', instance.name)
    instance.description = validated_data.get('description', instance.description)
    instance.end_date = validated_data.get('end_date', instance.end_date)
    instance.save()

    # update questions
    questions = validated_data.pop('questions')
    updated_questions_pks = list()

    for question_data in questions:
        if "pk" in question_data.keys(): # if 'pk' was supplied
            exists, question = instance_exists(Question, pk=question_data.get('pk'))
            if exists:
                update_question(question, question_data)
                updated_questions_pks.append(question.pk)
        else: # create question if 'pk' wan't supplied
            created_question = create_question(question_data, survey=instance)
            updated_questions_pks.append(created_question.pk)

    delete_not_updated_instances(instance.questions.all(), updated_questions_pks)

    return instance


def create_completed_survey(validated_data):
    """Creates completed survey 
    from the passed data.
    """
    answers = validated_data.pop('answers')
    completed_survey = CompletedSurvey.objects.create(**validated_data)

    for answer_data in answers:
        question = answer_data.get('question')

        answer_choices = answer_data.get('answer_choices')
        if not answer_choices and question.question_type in (2, 3):
            raise serializers.ValidationError("If you want to answer to not 'text answer' question, you must supply answer choices.")

        answer = Answer.objects.create(completed_survey=completed_survey, question=question)

        if question.question_type == 1: # Text answer
            answer.text_answer = answer_data.get('text_answer')
            answer.save()

        elif question.question_type == 2: # One choice answer
            answer.answer_choices.add(answer_choices[0])

        elif question.question_type == 3: # Multiple choices answer
            for answer_choice in answer_choices:
                answer.answer_choices.add(answer_choice)

    return completed_survey