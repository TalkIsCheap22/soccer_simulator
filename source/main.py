from event import League
from team import Team
from preprocess import Reader
import argparse

def __main__():
    parser = argparse.ArgumentParser(description="test")
    parser.add_argument('--in_file', type=str, default="../input/input.json")
    parser.add_argument('--out_dir', type=str, default="../output")
    args = parser.parse_args()

    reader = Reader(args.in_dir)
    dict = reader.convert_to_dictionary()
    league = League(dict)
    league.simulate()