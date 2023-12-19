from event import Tour
from team import Team
from preprocess import Reader
import argparse


parser = argparse.ArgumentParser(description="test")
parser.add_argument('--in_file', type=str, default="../input/input.json")
parser.add_argument('--out_dir', type=str, default="../output")
args = parser.parse_args()

reader = Reader(args.in_file)
dict = reader.convert_to_dictionary()
tour = Tour(dict)
print("--Tour created!--")
mci_champs = 0
for _ in range(100):
    tour.simulate()
    if tour.champion.name == "Manchester City":
        mci_champs += 1
    tour.restore()
print("Manchester City wins {a} champions in 100 tours".format(a=mci_champs))
    