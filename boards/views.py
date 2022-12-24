from django.http import HttpResponse, Http404
from django.shortcuts import render

from boards.models import Board


# Create your views here.
# def home(request):

    # return HttpResponse('Hello World')

    # boards = Board.objects.all()
    # boards_name = list()
    #
    # for i in boards:
    #     boards_name.append(i.name)
    #
    # response_html = '<br>'.join(boards_name)
    #
    # return HttpResponse(response_html)
def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})

def board_topics(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404
    return render(request, 'topics.html', {'board': board})