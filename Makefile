# overall account id
ACCOUNT_ID = 433122885944
ROLE_NAME = lambdaTestRole
# function name (which function? in our file, or in AWS lambda)
FUNCTION_NAME = testWorld
REGION = us-east-1
TIMEOUT = 15
MEMORY_SIZE = 128
ZIPFILE_NAME = lambda.zip
# filename.function where the lambda handler is located:
HANDLER = lambda-code.lambda_handler

clean:
	rm -rf __pycache__
	rm -rf ./libs/

install_deps :
	pip install --upgrade -r requirements.txt -t libs/

build : install_deps clean
	zip $(ZIPFILE_NAME) -r *

create : build
	aws lambda create-function --region $(REGION) --function-name $(FUNCTION_NAME) --zip-file fileb://$(ZIPFILE_NAME) --role arn:aws:iam::$(ACCOUNT_ID):role/$(ROLE_NAME)  --handler $(HANDLER) --runtime python2.7 --timeout $(TIMEOUT) --memory-size $(MEMORY_SIZE)

update: build
	aws lambda update-function-code --region $(REGION) --function-name $(FUNCTION_NAME) --zip-file fileb://$(ZIPFILE_NAME) --publish

deploy: update

.PHONY: test
test:
	python -W ignore -m unittest test_lambda
