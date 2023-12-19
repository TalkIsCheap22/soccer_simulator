from team import Team
import functools
import json

class Match:
    def __init__(self, home, away, round):
        self.home = home
        self.away = away
        self.round = round
        self.finish = False

    def print_res(self):
        if self.finish:
            print("{a1} {b1} - {b2} {a2}".format(a1=self.home.name, b1=self.home_goals, a2=self.away.name, b2=self.away_goals))
        else:
            print("The match has not finished!")

    def simulate(self):
        self.home_goals = self.home.cal_goals(1, self.away)
        self.away_goals = self.away.cal_goals(0, self.home)
        self.finish = True
        self.home.end_of_match(self.home_goals, self.away_goals)
        self.away.end_of_match(self.away_goals, self.home_goals)
        self.print_res()

class Tour:
    def __init__(self, dict):
        self.tot_rounds = dict["tot_rounds"]
        self.teams = []
        for item in dict["teams"]:
            team = Team(item)
            self.teams.append(team)
        self.ranking = self.teams
        self.scorer_list, self.assister_list = [], []
        avg_home_losses = float(sum([team.avg_home_losses for team in self.teams])) / len(self.teams)
        avg_away_losses = float(sum([team.avg_away_losses for team in self.teams])) / len(self.teams)
        for team in self.teams:
            self.scorer_list += team.players
            self.assister_list += team.players
            team.home_defence = avg_home_losses / team.avg_home_losses
            team.away_defence = avg_away_losses / team.avg_away_losses
        rounds, self.rounds = dict["rounds"], []
        home_team = self.teams[0]
        away_team = self.teams[1]
        for item in rounds:
            matches = []
            for m in item:
                for team in self.teams:
                    if team.name == m["home"]:
                        home_team = team
                    elif team.name == m["away"]:
                        away_team = team
                match = Match(home_team, away_team, m["round"]) 
                matches.append(match)
            self.rounds.append(matches)

    def print_ranking(self):
        print("Team:\t\tpoints")
        for team in self.ranking:
            print("{a} {b}".format(a=team.name, b=team.points))
    
    def points_cmp(self, a, b):
        if a.points == b.points:
            if a.diff == b.diff:
                return b.goals - a.goals    
            return b.diff - a.diff
        return b.points - a.points

    def update(self):
        self.ranking.sort(key=functools.cmp_to_key(self.points_cmp))
        self.scorer_list.sort(key=lambda s:s.goals, reverse=True)
        self.assister_list.sort(key=lambda s:s.goals, reverse=True)

    def play_a_round(self, round):
        curr_round = self.rounds[round - 1]
        for match in curr_round:
            match.simulate()
        self.update()
    
    def simulate(self):
        for i in range(self.tot_rounds):
            self.play_a_round(i+1)
        self.champion = self.ranking[0]
        self.print_ranking()
        print("The champion is {a}".format(a=self.champion.name))
        print("The player who scored most goals is {a}, who scored {b} goals".format(a=self.scorer_list[0].name,b=self.scorer_list[0].goals))

    def restore(self):
        for round in self.rounds:
            for match in round:
                match.finish = False
        for team in self.teams:
            team.restore()