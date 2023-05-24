from django import forms
from django.core.exceptions import ValidationError

from football.models import Comment, Match, Team


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class AddLeagueMatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['team_home', 'team_away', 'team_home_goals', 'team_away_goals', 'referee', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

    # check if teams are not the same and goals are positive values
    def clean(self):
        cleaned_data = super().clean()
        team_home = cleaned_data['team_home']
        team_away = cleaned_data['team_away']
        team_home_goals = cleaned_data['team_home_goals']
        team_away_goals = cleaned_data['team_away_goals']
        if team_home == team_away:
            raise ValidationError("The same teams can't play against each other")
        if team_home_goals < 0 or team_away_goals < 0:
            raise ValidationError("Goals have to be positive values")
        return cleaned_data

    # while creating a form view, the teams for selection will be automatically sorted by the league
    def __init__(self, *args, **kwargs):
        league = kwargs.pop('league')
        super().__init__(*args, **kwargs)
        self.fields['team_home'] = forms.ModelChoiceField(queryset=Team.objects.filter(league=league))
        self.fields['team_away'] = forms.ModelChoiceField(queryset=Team.objects.filter(league=league))
