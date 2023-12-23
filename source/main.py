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
tour.simulate()
tour.restore()

#<table class="min_width sortable stats_table min_width shade_zero"