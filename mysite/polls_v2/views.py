from django.http import HttpResponse
from .models import Question



"""def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)"""

"""  # update from code above
from django.template import loader  # added for html template load
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls_v2/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))"""

from django.shortcuts import render  # shortcut to render the context
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls_v2/index.html', context)


"""
from django.http import Http404
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls_v2/detail.html', {'question': question})"""
# Alternative for detail below, see https://docs.djangoproject.com/en/2.1/intro/tutorial03/ for more info


from django.shortcuts import get_object_or_404
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls_v2/detail.html', {'question': question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)