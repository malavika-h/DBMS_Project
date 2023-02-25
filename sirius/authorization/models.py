from django.db import models
from team.models import Team
from django.contrib.auth import get_user_model

class Role(models.Model):
    role_name = models.CharField(max_length=100)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    role_description = models.CharField(max_length=100)
    permissions = models.TextField(default="")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['role_name', 'team_id'], 
                name='unique_role_name_team_id'
            )
        ]

    def __str__(self):
        return self.role_name

class Membership(models.Model):
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    alumni = models.BooleanField(default=False)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE, default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'team_id'], 
                name='unique_user_id_team_id'
            )
        ]

    def __str__(self):
        return f'{self.user_id.username}-{self.team_id.name}'
        
class Permission(models.Model):
    ACTION_CHOICES = (
        ('C', 'Create'),
        ('R', 'Read'),
        ('U', 'Update'),
        ('D', 'Delete'),
        ('E', 'Edit'),
        ('V', 'View'),
    )
    RELATION_CHOICES = (
        ('T', 'Team'),
        ('R', 'Role'),
        ('C', 'Class'),
        ('N', 'Notice'),
        ('E', 'Event'),
        ('P', 'Project'),
        ('M', 'Membership'),
        ('JR', 'JoinRequest'),
        ('I', 'Invite'),
        ('TD', 'ToDo'),
        ('FA', 'FeedbackAnalysis'),
    )
    action = models.CharField("action", max_length=1, choices= ACTION_CHOICES)
    relation = models.CharField("relation", max_length=2, choices= RELATION_CHOICES)

    def __str__(self):
        return self.action + " " + self.relation
