from django.contrib import admin
from .models import Poll, Choice, Vote


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2  # Show 2 empty choice fields by default
    min_num = 2  # Require at least 2 choices
    max_num = 4  # Allow maximum 4 choices
    fields = ['text', 'vote_count']
    readonly_fields = ['vote_count']


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['question', 'poll_code', 'created_by', 'created_date', 'is_active', 'get_choice_count', 'get_total_votes']
    list_filter = ['is_active', 'created_date', 'created_by']
    search_fields = ['question', 'poll_code', 'created_by__username']
    readonly_fields = ['poll_code', 'created_date']
    inlines = [ChoiceInline]
    
    def get_choice_count(self, obj):
        return obj.choices.count()
    get_choice_count.short_description = 'Choices'
    
    def get_total_votes(self, obj):
        return obj.get_total_votes()
    get_total_votes.short_description = 'Total Votes'


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['text', 'poll', 'get_vote_count']
    list_filter = ['poll']
    search_fields = ['text', 'poll__question']
    
    def get_vote_count(self, obj):
        return obj.get_vote_count()
    get_vote_count.short_description = 'Vote Count'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'choice', 'get_poll', 'voted_at']
    list_filter = ['voted_at', 'choice__poll']
    search_fields = ['user__username', 'choice__text', 'choice__poll__question']
    readonly_fields = ['user', 'choice', 'voted_at']
    
    def get_poll(self, obj):
        return obj.choice.poll.question
    get_poll.short_description = 'Poll'

