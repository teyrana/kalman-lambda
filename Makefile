# Assumes that the remaining variables are set in the environment

include env.makefile

REGION = us-east-1
TIMEOUT = 15
MEMORY_SIZE = 128
ZIPFILE_NAME = lambda.zip
# filename.function where the lambda handler is located:
HANDLER = lambda_code.lambda_handler

clean:
	rm -rf __pycache__
	rm -rf ./libs/

install:
	pip install --upgrade -r requirements.txt -t libs/

build: clean
	docker build -t lambda:build-python3 .

debug: build
	docker run -it lambda:build-python3 bash

deploy: build
	docker run lambda:build-python3

.PHONY: test
test:
	python -W ignore -m unittest test_lambda
