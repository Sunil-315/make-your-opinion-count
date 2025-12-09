from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Poll, Choice


def create_poll(request):
    """View to create a new poll"""
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
        
        # Create poll
        poll = Poll.objects.create(question=question)
        
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
    
    context = {
        'poll': poll,
        'choices': choices,
        'total_votes': total_votes,
    }
    return render(request, 'polls/view_poll.html', context)


def vote(request, poll_code):
    """Handle voting on a poll"""
    poll = get_object_or_404(Poll, poll_code=poll_code)
    
    if request.method == 'POST':
        choice_id = request.POST.get('choice')
        
        if not choice_id:
            messages.error(request, 'Please select an option.')
            return redirect('polls:view_poll', poll_code=poll_code)
        
        try:
            choice = poll.choices.get(id=choice_id)
            choice.vote_count += 1
            choice.save()
            messages.success(request, 'Your vote has been recorded!')
        except Choice.DoesNotExist:
            messages.error(request, 'Invalid choice.')
        
        return redirect('polls:view_poll', poll_code=poll_code)
    
    return redirect('polls:view_poll', poll_code=poll_code)


def my_polls(request):
    """View to list all polls (can be filtered by user later)"""
    polls = Poll.objects.all()
    context = {
        'polls': polls,
    }
    return render(request, 'polls/my_polls.html', context)
