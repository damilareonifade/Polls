from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from polls.models import Option, Polls, Vote

from .forms import (CreatePollForm, EditPollForm, OptionEditForm,
                    OptionPollForm, RegisterForm)


def register(request):
    if request.method == 'POST':
        registerform = RegisterForm(request.POST)
        if registerform.is_valid():
            user = registerform.save(commit=False)
            user.email = registerform.cleaned_data['email']
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            user.email_user(subject=subject,message=message)
            return HttpResponse('registered succesfully and activation sent')
    else:
        registerform = RegisterForm(request.POST)
    return render(request,'accounts/register.html',{'form':registerform})

def activate(request,uidb64,token):
    try:
        uid= force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        login(request,user)
        return redirect('polls:list')

    else:
        return render(request, 'account/activation_invalid.html')


@login_required
def create_poll(request):
    if request.method == "POST":
        polls_form = CreatePollForm(request.POST)
        if polls_form.is_valid():
            polls = polls_form.save(commit=False)
            polls.author = request.user 
            polls.save()
            choice_text= Option(polls=polls,option = polls_form.cleaned_data['choice_text1']).save()
            choice_text2 = Option(polls=polls,option = polls_form.cleaned_data['choice_text2']).save()
            return redirect(reverse('polls:list'))

    else:
        polls_form = CreatePollForm(request.POST)
    return render(request,'accounts/user/create_polls.html',{'form':polls_form})

@login_required
def create_option(request,id):
    poll = get_object_or_404(Polls,id=id,is_active=True)
    if request.method == 'POST':
        option_form = OptionPollForm(request.POST)
        if option_form.is_valid:
            option_form = option_form.save(commit=False)
            option_form.polls = poll
            option_form.save()
        else:
            option_form = OptionPollForm()
    
    return render(request,'accounts/user/create_polls.html',{'option_form':option_form})

@login_required
def edit_poll(request,id):
    poll = get_object_or_404(Polls,id=id)
    if request.user != poll.author:
        return redirect('polls:list')

    if request.method == 'POST':
        form = EditPollForm(request.POST,instance=poll)
        if form.is_valid():
            form.save()
            return redirect('polls:list')
    return render(request,'accounts/user/edit_polls.html',{'form':form})

@login_required
def add_choice(request,id):
    polls = get_object_or_404(Polls,id=id)

    if request.user != polls.author:
        return redirect('polls:list')
    
    if request.method == 'POST':
        form = OptionPollForm(request.POST)
        if form.is_valid():
            new_choice = form.save(commit=False)
            new_choice.poll = polls.id 
            new_choice.save()
            return redirect('polls:edit',polls.id)
    
    else:
        form = OptionPollForm()    
    return render(request,'account/add_choice.html',{'form':form})


@login_required
def polls_delete(request,id):
    polls = get_object_or_404(Polls,id=id,is_active=True)

    if request.user != polls.author:        
        return redirect('polls:list')
    poll = polls.delete()
    return redirect('polls:list')

@login_required
def choice_edit(request,option_id):
    choice = get_object_or_404(Option,pk=option_id)
    poll = get_object_or_404(Polls,pk=choice.poll.id)
    if request.user != request.author:
        return redirect('polls.list')

    if request.method == 'POST':
        form = OptionEditForm(request.POST,instance=choice)
        if form.is_valid():
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            return redirect('polls:list')
    else:
        form = OptionEditForm(instance =choice)
    return render(request,'polls/add_choice.html',{'form':form})
    
@login_required
def vote(request,id):
    option_id = request.POST.get('choice')
    poll = get_object_or_404(Polls,id=id,is_active=True)
    options = poll.option_set.filter(option=option_id)
    option = poll.option._set.all()
    if Vote(poll=poll,option=options,user=request.user).exists():
        option = poll.option_set.all()
        option.option_count = F('option_count') - 1
        option.save()
        option.refresh_from_db()
    
        
    else:
        vote = Vote(poll=poll,option=options,user=request.user).save()
        option.option_count = F('option_count') + 1
        vote.save()
        vote.refresh_from_db()
        
