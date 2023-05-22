from football.models import Match, League, Team


def filter_teams_by_league(league_id):
    league = League.objects.get(pk=league_id)
    teams = Team.objects.filter(league=league)
    return teams


def filter_matches_by_league(league_id):
    league = League.objects.get(pk=league_id)
    matches = Match.objects.filter(league=league)
    return matches
