import numpy as np

class Player:
    def __init__(self, dict):
        self.name = ""

        self.prev_home_goals = dict["prev_home_goals"]
        self.prev_away_goals = dict["prev_away_goals"]
        self.prev_home_assists = dict["prev_home_assists"]
        self.prev_away_assists = dict["prev_away_assists"]
        self.goals = 0
        self.assist = 0

class Team:
    def __init__(self, dict):
        self.name = ""

        self.players = []
        for item in dict["players"]:
            player = Player(item)
            self.players.append(player)
        self.prev_home_goals = dict["prev_home_goals"]#let alone own goals
        self.prev_away_goals = dict["prev_away_goals"]
        self.prev_home_losses = dict["prev_home_losses"]
        self.prev_away_losses = dict["prev_away_losses"]
        self.prev_home_matches = dict["prev_home_matches"]
        self.prev_away_matches = dict["prev_away_matches"]
        self.avg_home_goals = self.prev_home_goals / self.prev_home_matches
        self.avg_away_goals = self.prev_away_goals / self.prev_away_matches
        self.avg_home_losses = self.prev_home_losses / self.prev_home_matches
        self.avg_away_losses = self.prev_away_losses / self.prev_away_matches
        self.goals = 0
        self.losses = 0
        self.diff = 0
        self.points = 0
        
        self.home_goal_dict, self.away_goal_dict, self.home_assist_dict, self.away_assist_dict = {}, {}, {}, {}
        for player in self.players:
            self.home_goal_dict[player.name] = player.prev_home_goals
            self.away_goal_dict[player.name] = player.prev_away_goals
            self.home_assist_dict[player.name] = player.prev_home_assists
            self.away_assist_dict[player.name] = player.prev_away_assists

    def rand_with_weight(tot, dict):
        ra, curr, ret = np.random.uniform(0,tot), 0, None
        for k in dict.keys:
            curr += dict[k]
            if ra <= curr:
                ret = k
                break
        return ret
    
    def scorer_assister(self, home):
        if home == 1:
            scorer = self.rand_with_weight(self.prev_home_goals, self.home_goal_dict)
            assister = self.rand_with_weight(self.prev_home_goals, self.home_assist_dict)
        else:
            scorer = self.rand_with_weight(self.prev_away_goals, self.away_goal_dict)
            assister = self.rand_with_weight(self.prev_away_goals, self.away_assist_dict)
        scorer.goals += 1
        if assister is not None:
            assister.assists += 1
    
    def cal_goals(self, home, oppo):
        goals = 0
        if home == 1:
            goals = np.random.poisson(lam=self.avg_home_goals/oppo.away_defence, size=1)
        else:
            goals = np.random.poisson(lam=self.avg_away_goals/oppo.home_defence, size=1)
        for _ in range(goals):
            self.scorer_assister(home)
        return goals
    
    def end_of_match(self, goals, oppo_goals):
        if goals > oppo_goals:
            self.points += 3
        elif goals == oppo_goals:
            self.points += 1
        self.goals += goals
        self.losses += oppo_goals
        self.diff = self.goals - self.losses