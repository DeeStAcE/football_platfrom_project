from football.models import Match, League, Team


# filter teams by entered league object
def filter_teams_by_league(league):
    teams = Team.objects.filter(league=league)
    return teams


# filter matches by entered league object
def filter_matches_by_league(league):
    matches = Match.objects.filter(league=league)
    return matches
