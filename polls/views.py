from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from django.db import IntegrityError
from .models import Poll, Choice, Vote


@login_required
def create_poll(request):
    """View to create a new poll - requires login"""
    if request.method == 'POST':
        question = request.POST.get('question', '').strip()
        
        # Collect all options
        options = []
        for i in range(1, 5):  # Check for option_1 through option_4
            option_text = request.POST.get(f'option_{i}', '').strip()
            if option_text:
                options.append(option_text)
        
        # Validation
        if not question:
            messages.error(request, 'Please provide a question for your poll.')
            return render(request, 'polls/create_poll.html')
        
        if len(options) < 2:
            messages.error(request, 'Please provide at least 2 options.')
            return render(request, 'polls/create_poll.html')
        
        if len(options) > 4:
            messages.error(request, 'Maximum 4 options allowed.')
            return render(request, 'polls/create_poll.html')
        
        # Create poll with current user as creator
        poll = Poll.objects.create(
            question=question,
            created_by=request.user
        )
        
        # Create choices
        for option_text in options:
            Choice.objects.create(poll=poll, text=option_text)
        
        messages.success(request, f'Poll created successfully! Poll code: {poll.poll_code}')
        return redirect('polls:view_poll', poll_code=poll.poll_code)
    
    return render(request, 'polls/create_poll.html')


def view_poll(request, poll_code):
    """View to display poll details and results"""
    poll = get_object_or_404(Poll, poll_code=poll_code)
    choices = poll.choices.all()
    total_votes = poll.get_total_votes()
    
    # Check if current user has voted
    has_voted = False
    user_vote = None
    if request.user.is_authenticated:
        has_voted = poll.user_has_voted(request.user)
        if has_voted:
            user_vote = Vote.objects.filter(choice__poll=poll, user=request.user).first()
    
    context = {
        'poll': poll,
        'choices': choices,
        'total_votes': total_votes,
        'has_voted': has_voted,
        'user_vote': user_vote,
    }
    return render(request, 'polls/view_poll.html', context)


def vote(request, poll_code):
    """Handle voting on a poll - requires login"""
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to vote.')
        return redirect('accounts:login')
    
    poll = get_object_or_404(Poll, poll_code=poll_code)
    
    if request.method == 'POST':
        # Check if user already voted
        if poll.user_has_voted(request.user):
            messages.error(request, 'You have already voted on this poll.')
            return redirect('polls:view_poll', poll_code=poll_code)
        
        choice_id = request.POST.get('choice')
        
        if not choice_id:
            messages.error(request, 'Please select an option.')
            return redirect('polls:view_poll', poll_code=poll_code)
        
        try:
            choice = poll.choices.get(id=choice_id)
            
            # Create vote record
            Vote.objects.create(user=request.user, choice=choice)
            messages.success(request, 'Your vote has been recorded! Thank you for participating.')
            
        except Choice.DoesNotExist:
            messages.error(request, 'Invalid choice.')
        except IntegrityError:
            messages.error(request, 'You have already voted on this poll.')
        
        return redirect('polls:view_poll', poll_code=poll_code)
    
    return redirect('polls:view_poll', poll_code=poll_code)


@login_required
def my_polls(request):
    """View to list all polls created by the current user - requires login"""
    polls = Poll.objects.filter(created_by=request.user).order_by('-created_date')
    
    context = {
        'polls': polls,
    }
    return render(request, 'polls/all_poll.html', context)

