from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import random
import string

class Poll(models.Model):
    question = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls', null=True, blank=True)
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
        return Vote.objects.filter(choice__poll=self).count()
    
    def get_results(self):
        """Get poll results with percentages"""
        total_votes = self.get_total_votes()
        results = []
        for choice in self.choices.all():
            vote_count = choice.votes.count()
            percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
            results.append({
                'choice': choice.text,
                'votes': vote_count,
                'percentage': round(percentage, 1)
            })
        return results
    
    def user_has_voted(self, user):
        """Check if a user has already voted on this poll"""
        if not user.is_authenticated:
            return False
        return Vote.objects.filter(choice__poll=self, user=user).exists()
    
    def __str__(self):
        return f"{self.question} ({self.poll_code})"
    
    class Meta:
        ordering = ['-created_date']


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    vote_count = models.IntegerField(default=0)  # Deprecated, use Vote model instead
    
    def get_vote_count(self):
        """Get actual vote count from Vote model"""
        return self.votes.count()
    
    def __str__(self):
        return f"{self.text} - {self.get_vote_count()} votes"
    
    class Meta:
        ordering = ['id']


class Vote(models.Model):
    """Track individual votes to prevent duplicate voting"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='votes')
    voted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'choice')
        # Ensure one vote per user per poll
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'choice'],
                name='unique_user_choice_vote'
            )
        ]
    
    def __str__(self):
        return f"{self.user.username} voted for {self.choice.text}"

