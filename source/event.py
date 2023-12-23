from team import Team
import functools
import json

class Match:
    def __init__(self, home, away, round):
        self.home = home
        self.away = away
        self.round = round
        self.finish = False

    def transfer_time(self, time):
        extra = 0
        if time > 45 and time < 51:
            extra = time - 45
            time = 45
        elif time > 95:
            extra = time - 95
            time = 90
        elif time > 50:
            time -= 5
        if extra == 0:
            return str(time)
        return ("{a}+{b}".format(a=time,b=extra))

    def print_res(self):
        if self.finish:
            tplt = "{0:^20}\t{1:^10}\t{2:^10}\t{3:^10}\t{4:^20}\t"
            print(tplt.format(self.home.name, self.home_goals, ":", self.away_goals, self.away.name))
            home_idx, away_idx, home_cnt, away_cnt, s = 0, 0, self.home_goals, self.away_goals, ""
            while home_idx < home_cnt and away_idx < away_cnt:
                if self.home_scorer_list[home_idx].minute <= self.away_scorer_list[away_idx].minute:
                    s = "{a}\' {b}".format(a=self.transfer_time(self.home_scorer_list[home_idx].minute),b=self.home_scorer_list[home_idx].scorer.name)
                    print(tplt.format(s, "", "", "", ""))
                    home_idx += 1
                else:
                    s = "{a}\' {b}".format(a=self.transfer_time(self.away_scorer_list[away_idx].minute),b=self.away_scorer_list[away_idx].scorer.name)
                    print(tplt.format("", "", "", "", s))
                    away_idx += 1
            if home_idx < home_cnt:
                for i in range(home_idx, home_cnt):
                    s = "{a}\' {b}".format(a=self.transfer_time(self.home_scorer_list[i].minute),b=self.home_scorer_list[i].scorer.name)
                    print(tplt.format(s, "", "", "", ""))
            else:
                for i in range(away_idx, away_cnt):
                    s = "{a}\' {b}".format(a=self.transfer_time(self.away_scorer_list[i].minute),b=self.away_scorer_list[i].scorer.name)
                    print(tplt.format("", "", "", "", s))
        else:
            #print("The match has not finished!")
            pass

    def simulate(self):
        self.home_goals, self.home_scorer_list = self.home.cal_goals(1, self.away)
        self.away_goals, self.away_scorer_list = self.away.cal_goals(0, self.home)
        self.finish = True
        self.home.end_of_match(self.home_goals, self.away_goals)
        self.away.end_of_match(self.away_goals, self.home_goals)
        self.print_res()

class Event:
    def __init__(self, dict):
        self.teams = []
        for item in dict["teams"]:
            team = Team(item)
            self.teams.append(team)
        self.scorer_list, self.assister_list = [], []
        avg_home_losses = float(sum([team.avg_home_losses for team in self.teams])) / len(self.teams)
        avg_away_losses = float(sum([team.avg_away_losses for team in self.teams])) / len(self.teams)
        for team in self.teams:
            self.scorer_list += team.players
            self.assister_list += team.players
            team.home_defence = avg_home_losses / team.avg_home_losses
            team.away_defence = avg_away_losses / team.avg_away_losses
     

    def print_scorer_list(self):
        tplt = "{0:^20}\t{1:^10}\t{2:^10}"
        print(tplt.format("Rank", "Player", "Goals"))
        cnt = 0
        for player in self.scorer_list:
            cnt += 1
            print(tplt.format(cnt, player.name, player.goals))
            if cnt == 30:
                return  

    def print_assister_list(self):
        tplt = "{0:^20}\t{1:^10}\t{2:^10}"
        print(tplt.format("Rank", "Player", "Assists"))
        cnt = 0
        for player in self.assister_list:
            cnt += 1
            print(tplt.format(cnt, player.name, player.assists))
            if cnt == 30:
                return

    def points_cmp(self, a, b):
        if a.points == b.points:
            if a.diff == b.diff:
                return b.goals - a.goals    
            return b.diff - a.diff
        return b.points - a.points

    def update(self):
        self.ranking.sort(key=functools.cmp_to_key(self.points_cmp))
        self.scorer_list.sort(key=lambda s:s.goals, reverse=True)
        self.assister_list.sort(key=lambda s:s.assists, reverse=True)

    def play_a_round(self, round):
        curr_round = self.rounds[round - 1]
        print("----Round {a}----".format(a=round))
        for match in curr_round:
            match.simulate()
        self.update()
    
    def simulate(self):
        for i in range(self.tot_rounds):
            self.play_a_round(i+1)
        self.champion = self.ranking[0]
        self.print_ranking()
        print("The champion is {a}".format(a=self.champion.name))
        self.print_scorer_list()
        self.print_assister_list()

    def restore(self):
        for round in self.rounds:
            for match in round:
                match.finish = False
        for team in self.teams:
            team.restore()


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
        self.rounds =  []
        for i in range(int(self.tot_rounds/2)):
            round = []
            for j in range(int(len(self.teams)/2)):
                match = Match(self.teams[j], self.teams[len(self.teams)-1-j], i + 1)
                round.append(match)
            temp = self.teams[len(self.teams)-1]
            for j in range(len(self.teams)-1, 1, -1):
                self.teams[j] = self.teams[j - 1]
            self.teams[1] = temp
            self.rounds.append(round)
        rounds = []
        for round in self.rounds:
            rounds.append(round)
        for round in rounds:
            new_round = []
            for match in round:
                new_match = Match(match.away, match.home, match.round + int(len(self.teams)/2))
                new_round.append(new_match)
            self.rounds.append(new_round)

    def print_ranking(self):
        tplt = "{0:^20}\t{1:^10}\t{2:^10}\t{3:^10}\t{4:^10}\t{5:^10}\t{6:^10}"
        print(tplt.format("Team", "Rank", "Points", "W/D/L", "Goals", "Losses", "Difference"))
        cnt = 0
        for team in self.ranking:
            cnt += 1
            WDL = "{a}/{b}/{c}".format(a=team.win,b=team.draw,c=team.defeat)
            print(tplt.format(team.name, cnt, team.points, WDL, team.goals, team.losses, team.diff))  

    def print_scorer_list(self):
        tplt = "{0:^20}\t{1:^10}\t{2:^10}"
        print(tplt.format("Rank", "Player", "Goals"))
        cnt = 0
        for player in self.scorer_list:
            cnt += 1
            print(tplt.format(cnt, player.name, player.goals))
            if cnt == 30:
                return  

    def print_assister_list(self):
        tplt = "{0:^20}\t{1:^10}\t{2:^10}"
        print(tplt.format("Rank", "Player", "Assists"))
        cnt = 0
        for player in self.assister_list:
            cnt += 1
            print(tplt.format(cnt, player.name, player.assists))
            if cnt == 30:
                return

    def points_cmp(self, a, b):
        if a.points == b.points:
            if a.diff == b.diff:
                return b.goals - a.goals    
            return b.diff - a.diff
        return b.points - a.points

    def update(self):
        self.ranking.sort(key=functools.cmp_to_key(self.points_cmp))
        self.scorer_list.sort(key=lambda s:s.goals, reverse=True)
        self.assister_list.sort(key=lambda s:s.assists, reverse=True)

    def play_a_round(self, round):
        curr_round = self.rounds[round - 1]
        print("----Round {a}----".format(a=round))
        for match in curr_round:
            match.simulate()
        self.update()
    
    def simulate(self):
        for i in range(self.tot_rounds):
            self.play_a_round(i+1)
        self.champion = self.ranking[0]
        self.print_ranking()
        print("The champion is {a}".format(a=self.champion.name))
        self.print_scorer_list()
        self.print_assister_list()

    def restore(self):
        for round in self.rounds:
            for match in round:
                match.finish = False
        for team in self.teams:
            team.restore()