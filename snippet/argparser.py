import argparse

# 등호(=)는 생략가능하다. 된다.
# python argparser.py -p=./test/tt1 -t=200
# python argparser.py -p ./test/tt1 -t 200
#


parser = argparse.ArgumentParser(description="argument parser sample")

parser.add_argument(
    '-t','--test', type=int, 
    default=100,
    help='help : it is test')
parser.add_argument('-p','--test-path', type=str, 
    default='./temp',
    help='help : it is test')

_args = parser.parse_args()

print(_args.test)
print(_args.test_path) # 매개변수 이름에 있는 -는 변수접근시 _ 로 바뀐다.
