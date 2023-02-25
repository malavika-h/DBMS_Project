from django import forms
from .models import Class, Notice, Event, Feedback


class ClassCreationForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ('start_time', 'end_time', 'day', 'title', 'team_id', 'description')
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'team_id': forms.HiddenInput(),
        }

    def clean(self):
        team_id = self.cleaned_data.get('team_id')
        start_time = self.cleaned_data.get('start_time')
        end_time = self.cleaned_data.get('end_time')
        day = self.cleaned_data.get('day')
        title = self.cleaned_data.get('title')

        if start_time and end_time and day and title:
            if start_time >= end_time:
                raise forms.ValidationError('Invalid time range')
            
            for _class in Class.objects.filter(day=day, team_id=team_id):
                if not (start_time >= _class.end_time or end_time <= _class.end_time):
                    raise forms.ValidationError('Class overlaps with another class')
        else:
            raise forms.ValidationError('Some fields are missing')

class ClassUpdationForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ('start_time', 'end_time', 'day', 'title', 'description')
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        start_time = self.cleaned_data.get('start_time')
        end_time = self.cleaned_data.get('end_time')
        day = self.cleaned_data.get('day')
        title = self.cleaned_data.get('title')
        team_id = self.instance.team_id

        if start_time and end_time and day and title:
            if start_time >= end_time:
                raise forms.ValidationError('Invalid time range')
            
            for _class in Class.objects.filter(day=day, team_id=team_id):
                if not (start_time >= _class.end_time or end_time <= _class.end_time):
                    raise forms.ValidationError('Class overlaps with another class')
        else:
            raise forms.ValidationError('Some fields are missing')


class CalendarCreationForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('start', 'end', 'title', 'description')
        widgets = {
            'start': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def clean(self):
        start = self.cleaned_data.get('start')
        end = self.cleaned_data.get('end')
        title = self.cleaned_data.get('title')

        if start and end and title:
            if Event.objects.filter(start=start, end=end, title=title).count() != 0:
                raise forms.ValidationError('Event already exists')
            if start >= end:
                raise forms.ValidationError('Invalid time range')
        else:
            raise forms.ValidationError('Some fields are missing')

class CalendarUpdationForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('start', 'end', 'title', 'description')
        widgets = {
            'start': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def clean(self):
        start = self.cleaned_data.get('start')
        end = self.cleaned_data.get('end')
        title = self.cleaned_data.get('title')

        if not start and not end and not title:
            raise forms.ValidationError('Some fields are missing')
        if start >= end:
            raise forms.ValidationError('Invalid time range')
        

class NoticeCreationForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ('title', 'description')
        
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError('Title of the notice is required')
        return title

class NoticeUpdationForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ('title', 'description')

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError('Title of the notice is required')
        return title

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('feedback',)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError('Title of the notice is required')
        return title


