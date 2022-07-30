from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import *


def home(request):
    return render(request,'polls/home.html')

def poll_list(request):
    all_polls = Polls.objects.filter(is_active=True)
    search_term = ''
    if 'search' in request.GET:
        search_term = request.GET('search_term')
        all_polls = Polls.objects.filter(title_icontain=search_term)
    
    paginator = Paginator(all_polls, 6)  # Show 6 contacts per page
    page = request.GET.get('page')
    polls = paginator.get_page(page)

    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
    print(params)
    return render(request,'polls/list.html',{'polls':polls,'search_term':search_term})

@login_required
def poll_details(request,id):
    polls = get_object_or_404(Polls, pk=id,is_active=True)
    return render(request,'polls/polls_details.html',{'polls':polls})

