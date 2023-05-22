from django.db import models
from django.utils.translation import gettext_lazy as _


class League(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class TeamFormation(models.Model):
    name = models.CharField(max_length=12)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=64)
    year = models.IntegerField()
    league = models.ManyToManyField(League, through='TeamLeague')
    formation = models.ForeignKey(TeamFormation, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class TeamLeague(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)


class Referee(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Match(models.Model):
    team_home = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_home')
    team_away = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_away')
    team_home_goals = models.SmallIntegerField()
    team_away_goals = models.SmallIntegerField()
    referee = models.ForeignKey(Referee, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return f'{self.team_home} {self.team_home_goals} : {self.team_away_goals} {self.team_away}'


class Player(models.Model):
    class Position(models.TextChoices):
        COACH = 'coach', _('Coach')
        GOALKEEPER = 'gk', _('Goalkeeper')
        DEFENDER = 'def', _('Defender')
        MIDFIELDER = 'mid', _('Midfielder')
        STRIKER = 'st', _('Striker')

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    position = models.CharField(choices=Position.choices)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
