import sys
from proj1_naive import naive
from proj1 import pyramid

if __name__ == '__main__':
	if len(sys.argv) <= 2:
		print(sys.argv)
		raise Exception("Method takes in image name, method (naive or pyramid), e.g. python main.py img.jpg naive")
	img = sys.argv[1]
	method = sys.argv[2]
	if method not in ('naive', 'pyramid'):
		raise Exception("Method must be stated as either naive or pyramid")
	if method == 'naive':
		naive(img)
	elif method == 'pyramid':
		pyramid(img)