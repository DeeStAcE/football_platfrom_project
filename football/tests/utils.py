from football.models import Match, League, Team


# filter teams by entered league object
def filter_teams_by_league(league):
    teams = Team.objects.filter(league=league)
    return teams


# filter matches by entered league object
def filter_matches_by_league(league):
    matches = Match.objects.filter(league=league)
    return matches


# filter comments by entered match object
def filter_comments_by_match(match):
    comments = match.comment_set.all()
    return comments
