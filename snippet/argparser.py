import argparse

parser = argparse.ArgumentParser(description="argument parser sample")

parser.add_argument('--test', type=int, 
    default=100,
    help='help : it is test')

_args = parser.parse_args()

print(_args.test)
