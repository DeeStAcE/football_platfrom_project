from django import forms
from django.db.models import Q

from football.models import Comment, Match, Team, PlayerGoals, Player


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

    # while creating a form view, the teams for selection will be automatically sorted by the league
    def __init__(self, *args, **kwargs):
        league = kwargs.pop('league')
        super().__init__(*args, **kwargs)
        self.fields['team_home'] = forms.ModelChoiceField(queryset=Team.objects.filter(league=league))
        self.fields['team_away'] = forms.ModelChoiceField(queryset=Team.objects.filter(league=league))


class AddLeagueMatchScorersForm(forms.ModelForm):
    class Meta:
        model = PlayerGoals
        fields = ['scorer']

    def __init__(self, *args, **kwargs):
        team_home = kwargs.pop('team_home')
        team_away = kwargs.pop('team_away')
        super().__init__(*args, **kwargs)
        self.fields['scorer'] = forms.ModelChoiceField(
            queryset=Player.objects.filter(Q(team=team_home) | Q(team=team_away)))
