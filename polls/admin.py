from django.contrib import admin
from .models import Poll, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2  # Show 2 empty choice fields by default
    min_num = 2  # Require at least 2 choices
    max_num = 4  # Allow maximum 4 choices
    fields = ['text', 'vote_count']
    readonly_fields = ['vote_count']


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['question', 'poll_code', 'created_date', 'is_active', 'get_choice_count', 'get_total_votes']
    list_filter = ['is_active', 'created_date']
    search_fields = ['question', 'poll_code']
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
    list_display = ['text', 'poll', 'vote_count']
    list_filter = ['poll']
    search_fields = ['text', 'poll__question']
    readonly_fields = ['vote_count']
