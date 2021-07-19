from django.core.paginator import Paginator
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404

from pybo.forms import QuestionForm
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

def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # answer = Answer(content=request.POST.get('content'), create_date=timezone.now())
    # answer.save()
    question.answer_set.create(content=request.POST.get('content'),
                               create_date=timezone.now())

    return redirect('pybo:detail', question_id=question_id)

def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            questoin = form.save(commit=False)
            questoin.create_date = timezone.now()
            questoin.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    return render(request, 'pybo/question_form.html', {'form': form})
