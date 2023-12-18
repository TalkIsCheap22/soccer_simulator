from team import Team
import functools

class Match:
    def __init__(self, home, away, round):
        self.home = home
        self.away = away
        self.round = round
        self.finish = False

    def print_res(self):
        if self.finish:
            print("{a1} {b1} {b2} {a2}".format(a1=self.home, b1=self.home_goals, a2=self.away, b2=self.away_goals))
        else:
            print("The match has not finished!")

    def simulate(self):
        self.home_goals = self.home.cal_goals(self.away)
        self.away_goals = self.away.cal_goals(self.home)
        self.finish = True
        self.home.end_of_match(self.home_goals, self.away_goals)
        self.away.end_of_match(self.away_goals, self.home_goals)
        self.print_res()

class League:
    def __init__(self, dict):
        self.tot_rounds = dict["tot_rounds"]
        self.teams = []
        for item in dict["teams"]:
            team = Team(item)
            self.teams.append(team)
        self.rounds = []
        self.ranking = self.teams
        self.team_idx = []
        self.scorer_list, self.assister_list = [], []
        avg_home_losses = sum([team.avg_home_losses for team in self.teams]) / len(self.teams)
        avg_away_losses = sum([team.avg_away_losses for team in self.teams]) / len(self.teams)
        for team in self.teams:
            self.scorer_list += team.players
            self.assister_list += team.players
            team.home_defence = team.avg_home_losses / avg_home_losses
            team.away_defence = team.avg_away_losses / avg_away_losses
        for i in range(self.tot_rounds):
            pass

    def print_ranking(self):
        print("Team:\t\tpoints")
        for team in self.ranking:
            print("{a}\t\t{b}".format(a=team.name, b=team.points))
    
    def points_cmp(a,b):
        if a.points == b.points:
            if a.diff == b.diff:
                return a.goals - b.goals    
            return a.diff - b.diff
        return a.points - b.points

    def update(self):
        self.rankings.sort(key=functools.cmp_to_key(self.points_cmp))
        self.scorer_list.sort(key=lambda s:s.goals, reverse=True)
        self.assister_list.sort(key=lambda s:s.goals, reverse=True)

    def play_a_round(self, round):
        curr_round = []
        for i in range(0, self.team_numbers, 2):
            match = Match(self.teams[i], self.teams[i+1], round)
            match.simulate()
            curr_round.append(Match)
        self.rounds.append(curr_round)
        self.update()
    
    def simulate(self):
        for i in range(self.tot_rounds):
            self.play_a_round(i + 1)
            #next_permutation
        self.champion = self.ranking[0]
        print("The champion is {a}".format(a=self.champion.name))
        print("The player who scored most goals is {a}, who scored {b} goals".format(a=self.scorer_list[0].name,b=self.scorer_list[0].goals))