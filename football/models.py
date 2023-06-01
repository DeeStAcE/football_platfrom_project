from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
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
    points = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.team} -> {self.league}'


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
    goal_scorers = models.ManyToManyField('Player', through='PlayerGoals')

    def __str__(self):
        return f'{self.team_home} {self.team_home_goals} : {self.team_away_goals} {self.team_away}'


class PlayerGoals(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    scorer = models.ForeignKey('Player', on_delete=models.CASCADE)
    goal = models.SmallIntegerField(default=1)
    minute = models.SmallIntegerField()


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


class Comment(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=False)


class UserRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # favourite team
    fav_team = models.ForeignKey(Team, on_delete=models.CASCADE)
