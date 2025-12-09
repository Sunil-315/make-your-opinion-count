from django.db import models
from django.core.exceptions import ValidationError
import random
import string

class Poll(models.Model):
    question = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    poll_code = models.CharField(max_length=8, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        # Generate unique poll code if not exists
        if not self.poll_code:
            self.poll_code = self.generate_poll_code()
        super().save(*args, **kwargs)
    
    def generate_poll_code(self):
        """Generate a unique 8-character poll code"""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if not Poll.objects.filter(poll_code=code).exists():
                return code
    
    def clean(self):
        """Validate that poll has between 2-4 choices"""
        super().clean()
        if self.pk:  # Only validate if poll already exists
            choice_count = self.choices.count()
            if choice_count < 2:
                raise ValidationError('A poll must have at least 2 choices.')
            if choice_count > 4:
                raise ValidationError('A poll can have a maximum of 4 choices.')
    
    def get_total_votes(self):
        """Get total number of votes across all choices"""
        return sum(choice.vote_count for choice in self.choices.all())
    
    def get_results(self):
        """Get poll results with percentages"""
        total_votes = self.get_total_votes()
        results = []
        for choice in self.choices.all():
            percentage = (choice.vote_count / total_votes * 100) if total_votes > 0 else 0
            results.append({
                'choice': choice.text,
                'votes': choice.vote_count,
                'percentage': round(percentage, 1)
            })
        return results
    
    def __str__(self):
        return f"{self.question} ({self.poll_code})"
    
    class Meta:
        ordering = ['-created_date']


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    vote_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.text} - {self.vote_count} votes"
    
    class Meta:
        ordering = ['id']
