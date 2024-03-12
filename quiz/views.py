import json
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Sources, Quiz
from django.views.generic import ListView, View
from .forms import ConfigForm1, ConfigForm2
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
import urllib.parse  # for encoding json data to pass url
from django import template
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
import requests
import html
import random
from .forms import CATEGORY_CHOICES_2
import datetime as dt

register = template.Library()

quiz_configurations = {
    'amount': None,
    'category': None,
    'difficulty': None,
    'type': None,
}


@register.filter  # for encoding dictionary(configurations) for url
def get_encoded_dict(data_dict):
    return urllib.urlencode(data_dict)


def shuffle_answers(correct_answer, incorrect_answers):
    answer_bank = [correct_answer, incorrect_answers[0], incorrect_answers[1], incorrect_answers[2]]
    random.shuffle(answer_bank)
    return answer_bank


def score_calculator(source_slug, quiz_data, user_answers):
    score = 0
    question_amount = len(quiz_data)
    mistakes = {}
    if source_slug == 'open-trivia-database-api':
        for n in range(0, question_amount):
            key = f'Q{n+1}'
            if quiz_data[n]['correct_answer'] == user_answers[key][0]['answer']:
                score += 1
            else:
                mistakes[key] = {
                    'question': quiz_data[n]['question'],
                    'user_answer': user_answers[key][0]['answer'],
                    'correct_answer': quiz_data[n]['correct_answer']
                }
    elif source_slug == 'the-trivia-api':
        for n in range(0, question_amount):
            key = f'Q{n+1}'
            if quiz_data[n]['correctAnswer'] == user_answers[key][0]['answer']:
                score += 1
            else:
                mistakes[key] = {
                    'question': quiz_data[n]['question']['text'],
                    'user_answer': user_answers[key][0]['answer'],
                    'correct_answer': quiz_data[n]['correctAnswer']
                }
    results = {
        'score': score,
        'mistakes': mistakes,
    }
    return results


class SourceListView(ListView):
    model = Sources
    template_name = 'quiz/quiz_list.html'
    context_object_name = 'sources'


class API_ConfigView(LoginRequiredMixin, View):
    template_name = 'quiz/config.html'
    success_url = '/solve'

    def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        if 'config_form_1' not in kwargs:
            kwargs['config_form_1'] = ConfigForm1()
        if 'config_form_2' not in kwargs:
            kwargs['config_form_2'] = ConfigForm2()
        # context['config_form'] = context['form']  # Set the context object name to 'config_form'
        return kwargs

    def post(self, request, *args, **kwargs):
        # config_form = ConfigForm1(request.POST)
        # if config_form.is_valid():
        #     print(config_form.data.get('amount'))
        #     print(config_form.data.get('category'))
        #     print(config_form.data.get('difficulty'))
        #     print(config_form.data.get('type'))
        #     return render(request, 'quiz/quiz_list.html')
        # else:
        #     return redirect('api_config')
        global quiz_configurations
        ctxt = {}

        if 'config_1' in request.POST:
            config_form_1 = ConfigForm1(request.POST)

            if config_form_1.is_valid():
                slug = self.get_object()
                quiz_configurations['amount'] = config_form_1.data.get('amount')
                quiz_configurations['category'] = config_form_1.data.get('category')
                quiz_configurations['difficulty'] = config_form_1.data.get('difficulty')
                quiz_configurations['type'] = config_form_1.data.get('type')
                parameters = {
                    'limit': quiz_configurations['amount'],
                    'categories': quiz_configurations['category'],
                    'difficulties': quiz_configurations['difficulty'],
                    'types': quiz_configurations['type'],
                }
                TheTRIVIA_URL = "https://the-trivia-api.com/v2/questions"
                print('config_form_1')  ###

                response = requests.get(url=TheTRIVIA_URL, params=parameters)
                json_data = response.json()

                # saving new quiz into Quiz model
                source_name = get_object_or_404(Sources, slug=slug)
                new_quiz = config_form_1.save(commit=False)
                new_quiz.source_name = source_name
                new_quiz.quiz_data = json_data
                new_quiz.user = request.user
                new_quiz.save()

                # Encode the JSON data into a query parameter
                json_data_encoded = urllib.parse.quote(json.dumps(json_data))
                query_params = '?json_data=' + json_data_encoded

                return redirect(reverse('source_solve', kwargs={'source_slug': slug}) + query_params)
            else:
                ctxt['config_form_1'] = config_form_1

        elif 'config_2' in request.POST:
            config_form_2 = ConfigForm2(request.POST)

            if config_form_2.is_valid():
                slug = self.get_object()
                quiz_configurations['amount'] = config_form_2.data.get('amount')
                quiz_configurations['difficulty'] = config_form_2.data.get('difficulty')
                quiz_configurations['category'] = config_form_2.data.get('category')
                quiz_configurations['type'] = config_form_2.data.get('type')
                parameters = {
                    'amount': quiz_configurations['amount'],
                    'category': quiz_configurations['category'],
                    'difficulty': quiz_configurations['difficulty'],
                    'type': quiz_configurations['type'],
                }
                OPENTDB_URL = "https://opentdb.com/api.php"
                print('config_form_2')  ###

                response = requests.get(url=OPENTDB_URL, params=parameters)
                json_data = response.json()

                if json_data['response_code'] == 1:
                    for category in CATEGORY_CHOICES_2:
                        if category[0] == int(quiz_configurations['category']):
                            messages.success(request, f"No quiz of category {category[1].upper()} in database")
                    return redirect('api_config', source_slug, source_object.id)

                # saving new quiz into Quiz model
                source_name = get_object_or_404(Sources, slug=slug)
                new_quiz = config_form_2.save(commit=False)
                new_quiz.source_name = source_name
                new_quiz.quiz_data = json_data['results']
                new_quiz.user = request.user
                new_quiz.save()

                # Encode the JSON data into a query parameter
                json_data_encoded = urllib.parse.quote(json.dumps(json_data))
                query_params = '?json_data=' + json_data_encoded

                # Redirect to SolveView with JSON data as query parameter
                return redirect(reverse('source_solve', kwargs={'source_slug': slug}) + query_params)
            else:
                ctxt['config_form_2'] = config_form_2

        return render(request, self.template_name, self.get_context_data(**ctxt))

    def get_object(self):  # to get slug from url
        slug = self.kwargs.get('source_slug')
        return slug

    def get(self, request, *args, **kwargs):
        slug = self.get_object()
        source_name = get_object_or_404(Sources, slug=slug)
        source_id = kwargs.get('pk')
        if int(source_id) == 1:
            config_form_1 = ConfigForm1()
            print("GET config_form_1")
            return render(request, 'quiz/config.html',
                          {'config_form_1': config_form_1, 'source_name': source_name, "source_id": source_id})
        elif int(source_id) == 2:
            config_form_2 = ConfigForm2()
            print("GET config_form_2")
            return render(request, 'quiz/config.html',
                          {'config_form_2': config_form_2, 'source_name': source_name, "source_id": source_id})


class SolveView(LoginRequiredMixin, View):
    template_name = 'quiz/quiz_solve.html'

    def get_object(self):
        slug = self.kwargs.get('source_slug')
        return slug

    def get(self, request, *args, **kwargs):
        json_data_encoded = request.GET.get('json_data', None)
        answer_data = []
        if json_data_encoded:
            try:
                json_data = json.loads(json_data_encoded)
                print(json_data)
                source_slug = self.get_object()
                source_object = get_object_or_404(Sources, slug=source_slug)
                source_id = source_object.id
                if source_object.name == "Open Trivia Database API":
                    results = json_data['results']
                    # if json_data['response_code'] == 1:
                    #     for category in CATEGORY_CHOICES_2:
                    #         if category[0] == int(quiz_configurations['category']):
                    #             messages.success(request, f"No quiz of category {category[1].upper()} in database")
                    #     return redirect('api_config', source_slug, source_object.id)
                    question_amount = len(results)
                    print('hi')
                    for question_data in results:
                        incorrect_answers = question_data['incorrect_answers']
                        correct_answer = question_data['correct_answer']
                        shuffled_answers = shuffle_answers(correct_answer, incorrect_answers)
                        answer_data.append(shuffled_answers)
                        question_data['question'] = html.unescape(question_data['question'])
                    print(results[0]['question'])
                    print(answer_data)
                    return render(request, 'quiz/quiz_solve.html',
                                  {'source_name': source_object.name, 'quiz_data': results,
                                   'shuffled_answers': answer_data, 'source_id': source_id,
                                   'question_amount': question_amount, 'source_slug': source_slug})
                elif source_object.name == "The Trivia API":
                    results = json_data
                    question_amount = len(results)
                    for question_data in results:
                        incorrect_answers = question_data['incorrectAnswers']
                        correct_answer = question_data['correctAnswer']
                        shuffled_answers = shuffle_answers(correct_answer, incorrect_answers)
                        answer_data.append(shuffled_answers)
                        question_data['question']['text'] = html.unescape(question_data['question']['text'])

                    return render(request, 'quiz/quiz_solve.html',
                                  {'source_name': source_object.name, 'quiz_data': results,
                                   'shuffled_answers': answer_data, 'question_amount': question_amount,
                                   'source_slug': source_slug, 'source_id': source_id})
            except json.JSONDecodeError as e:
                return HttpResponse("Error decoding JSON data", status=400)
        else:
            return HttpResponse("No JSON data provided", status=400)

    def post(self, request, *args, **kwargs):
        print('hello')
        if request.method == "POST":
            user_answers = json.loads(request.body)  # parse the JSON data into a dictionary
            source_slug = kwargs.get('source_slug')
            quiz_object = Quiz.objects.last()
            quiz_data = quiz_object.quiz_data
            results = score_calculator(source_slug, quiz_data, user_answers)
            # saving user answers and score
            time = dt.datetime.now().strftime("%Y-%m-%d")
            quiz_object.user_answers = user_answers
            quiz_object.solved = time
            quiz_object.user_score = results['score']
            quiz_object.save()
            quiz_object.user_mistakes = results['mistakes']
            return JsonResponse(
                {
                    "success": True,
                    "quiz_title": quiz_object.quiz_data[0]['category'].capitalize(),
                    "score": results['score'],
                    "mistakes": results['mistakes'],
                }
            )
