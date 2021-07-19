from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404

from pybo.forms import QuestionForm, AnswerForm
from pybo.models import Question, Answer


def index(request):
    page = request.GET.get('page', '1')

    question_list = list(Question.objects.order_by('-create_date'))

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}

    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}

    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now();
            answer.question = question
            answer.author = request.user
            answer.save()
            return redirect('pybo:detail', question_id=question_id)

    return redirect('pybo:detail', question_id=question_id)

@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.author = request.user
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    return render(request, 'pybo/question_form.html', {'form': form})
