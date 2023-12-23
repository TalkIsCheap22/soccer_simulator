import numpy as np

class Player:
    def __init__(self, dict):
        self.name = dict["name"]

        self.prev_goals = dict["prev_goals"]
        self.prev_assists = dict["prev_assists"]
        self.goals = 0
        self.assists = 0

    def restore(self):
        self.goals = 0
        self.assists = 0        

   # def __hash__(self):
   #     return 27 * 27 * (ord(self.name[0]) - ord('A')) + 27 * (ord(self.name[1]) - ord('a')) + ord(self.name[2]) - ord('a')

class Goal:
    def __init__(self,dict):
        self.scorer = dict["scorer"]
        self.assister = dict["assister"]
        self.minute = dict["minute"]
        self.home = 1

class Team:
    def __init__(self, dict):
        self.name = dict["name"]

        self.players = []
        for item in dict["players"]:
            player = Player(item)
            self.players.append(player)
        self.prev_home_goals = dict["prev_home_goals"]#let alone own goals
        self.prev_away_goals = dict["prev_away_goals"]
        self.prev_goals = self.prev_home_goals + self.prev_away_goals
        self.prev_home_losses = dict["prev_home_losses"]
        self.prev_away_losses = dict["prev_away_losses"]
        self.prev_home_matches = dict["prev_home_matches"]
        self.prev_away_matches = dict["prev_away_matches"]
        self.avg_home_goals = float(self.prev_home_goals) / self.prev_home_matches
        self.avg_away_goals = float(self.prev_away_goals) / self.prev_away_matches
        self.avg_home_losses = float(self.prev_home_losses) / self.prev_home_matches
        self.avg_away_losses = float(self.prev_away_losses) / self.prev_away_matches
        self.goals = 0
        self.losses = 0
        self.goals_list = []
        self.diff = 0
        self.points = 0
        self.win, self.defeat, self.draw = 0, 0, 0
        
        self.goals_dict, self.assists_dict = {}, {}
        for player in self.players:
            self.goals_dict[player.name] = player.prev_goals
            self.assists_dict[player.name] = player.prev_assists

    def get_player(self, name):
        for player in self.players:
            if player.name == name:
                return player

    def rand_with_weight(self, tot, dict):
        ra, curr, ret = np.random.uniform(0,tot), 0, None
        for k in dict.keys():
            curr += dict[k]
            if ra <= curr:
                ret = k
                break
        return ret
    
    def score_time(self, num):
        rand = np.random.uniform(0,100,size=num)
        rand.sort()
        rand = list(map(lambda x:int(x) + 1, rand))
        return rand
    
    def scorer_assister(self):
        scorer = self.get_player(self.rand_with_weight(self.prev_goals, self.goals_dict))
        assister = self.get_player(self.rand_with_weight(self.prev_goals, self.assists_dict))
        if scorer is None:
            #scorer = self.players[0]
            scorer = np.random.choice(self.players)
        scorer.goals += 1
        if assister is not None:
            while assister is None or assister.name == scorer.name:
                assister = self.get_player(self.rand_with_weight(self.prev_goals, self.assists_dict))
            #print("{a} assists {b}".format(a=assister.name,b=scorer.name))
            assister.assists += 1
        return scorer, assister
    
    def cal_goals(self, home, oppo):
        goals = 0
        if home == 1:
            goals = np.random.poisson(lam=float(self.avg_home_goals)/oppo.away_defence, size=1)[0]
        else:
            goals = np.random.poisson(lam=float(self.avg_away_goals)/oppo.home_defence, size=1)[0]
        scorer_list, assister_list, match_goal_list = [], [], []
        for _ in range(goals):
            scorer, assister = self.scorer_assister()
            scorer_list.append(scorer)
            assister_list.append(assister)
        times = self.score_time(goals)
        for i in range(goals):
            goal = Goal({"scorer": scorer_list[i], "assister": assister_list[i], "minute": times[i], "home": home})
            self.goals_list.append(goal)
            match_goal_list.append(goal)
        return goals, match_goal_list
    
    def end_of_match(self, goals, oppo_goals):
        if goals > oppo_goals:
            self.points += 3
            self.win += 1
        elif goals == oppo_goals:
            self.points += 1
            self.draw += 1
        else:
            self.defeat += 1
        self.goals += goals
        self.losses += oppo_goals
        self.diff = self.goals - self.losses

    def restore(self):
        self.goals = 0
        self.losses = 0
        self.diff = 0
        self.points = 0
        self.win, self.defeat, self.draw = 0, 0, 0
        self.goals_list = []
        for player in self.players:
            player.restore()