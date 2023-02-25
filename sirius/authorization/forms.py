from django import forms
from .models import Role,Membership
from team.models import Team

class RoleCreationForm(forms.ModelForm):
    class Meta:
        widgets = {
            'team_id': forms.HiddenInput(),
        }
        model = Role
        fields = ('role_name', 'team_id')

    # def clean_team_id(self):
    #     team_id = self.cleaned_data.get('team_id')
    #     if not Team.objects.filter(id=team_id).exists():
    #         raise forms.ValidationError('Invalid Team id')
    #     team = Team.objects.get(id=team_id)
    #     return team

class MembershipUpdationForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ('user_id', 'role_id')
