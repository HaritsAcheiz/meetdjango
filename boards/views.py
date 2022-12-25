from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

from boards.models import Board


# Create your views here.
def home(request):
    # try print Hello world
    # return HttpResponse('Hello World')

    #try print list of board name without template html file
    # boards = Board.objects.all()
    # boards_name = list()
    #
    # for i in boards:
    #     boards_name.append(i.name)
    #
    # response_html = '<br>'.join(boards_name)
    #
    # return HttpResponse(response_html)

    #render list of boards with template html file
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})

def board_topics(request, pk):
    # without shortcut
    # try:
    #     board = Board.objects.get(pk=pk)
    # except Board.DoesNotExist:
    #     raise Http404

    #with shortcut
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board': board})