import argparse

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('--path', metavar='p', type=str,
                    help='Process path')

args = parser.parse_args()