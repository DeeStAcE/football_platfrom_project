def assign_points_to_winning_team(league, team_home, team_away, team_home_goals, team_away_goals):
    if team_home_goals > team_away_goals:
        pass
        team = team_home.teamleague_set.get(league=league)
        team.points += 3
        team.save()
    elif team_home_goals < team_away_goals:
        team = team_away.teamleague_set.get(league=league)
        team.points += 3
        team.save()
    else:
        team1 = team_home.teamleague_set.get(league=league)
        team1.points += 1
        team1.save()
        team2 = team_away.teamleague_set.get(league=league)
        team2.points += 1
        team2.save()
