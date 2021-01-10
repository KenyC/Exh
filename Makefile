

all: example test

example:
	cd examples && make

test: 
	cd tests && bash test