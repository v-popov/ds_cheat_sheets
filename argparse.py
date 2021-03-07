import argparse

parser = argparse.ArgumentParser(description='''Some Description''', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-fa', '--first_arg', default=1, type=int, help='''First Argument''')
parser.add_argument('-od', '--output_directory', default='/home/myproject/', type=str, help='Output folder')

if name == 'main':
    args = parser.parse_args()
    print(f'This is first argument: {args.first_arg}')


# (base) C:\path_to_script>python scratch_1.py -h
# usage: scratch_1.py [-h] [-fa FIRST_ARG] [-od OUTPUT_DIRECTORY]
#
# Some Description
#
# optional arguments:
#   -h, --help            show this help message and exit
#   -fa FIRST_ARG, --first_arg FIRST_ARG
#                         First Argument
#   -od OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
#                         Output folder
#
# (base) C:\path_to_script>python scratch_1.py -fa=123
# This is first argument: 123