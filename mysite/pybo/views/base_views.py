from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404

from pybo.models import Question, Answer


def index(request):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')  # 정렬기준

    question_list = Question.objects.order_by('-create_date')

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.objects.order_by('-create_date')

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
        ).distinct()

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so':so}

    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    page = request.GET.get('page', '1')

    question = get_object_or_404(Question, pk=question_id)
    answer_list = Answer.objects.filter(question=question).order_by('-create_date')

    paginator = Paginator(answer_list, 5)
    page_obj = paginator.get_page(page)

    context = {'question': question, 'answer_list': page_obj}

    return render(request, 'pybo/question_detail.html', context)