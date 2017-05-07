# this makefile will be run within the docker container

# this file needs to be created *OUTSIDE THE REPO* :
#   it will contain authentication info, and should be kept safe
include env.makefile

REGION = us-east-1
TIMEOUT = 15
MEMORY_SIZE = 128
ZIPFILE_NAME = lambda.zip
# filename.function where the lambda handler is located:
HANDLER = lambda_code.lambda_handler

clean :
	rm -rf __pycache__
	rm -rf ./libs/

install_deps : clean
	pip install --upgrade -r requirements.txt -t libs/

build : install_deps
	zip $(ZIPFILE_NAME) -r *

configure: build
	echo "configuring aws..."
	aws configure set aws_access_key_id $(AZN_KEY_ID)
	aws configure set aws_secret_access_key $(AZN_SECRET_KEY)

create: configure
	aws lambda create-function --region $(REGION) --function-name $(FUNCTION_NAME) --zip-file fileb://$(ZIPFILE_NAME) --role arn:aws:iam::$(ACCOUNT_ID):role/$(ROLE_NAME)  --handler $(HANDLER) --runtime python3.6 --timeout $(TIMEOUT) --memory-size $(MEMORY_SIZE)

deploy: configure
	echo "updating aws lambda function..."
	aws lambda update-function-code --region $(REGION) --function-name $(FUNCTION_NAME) --zip-file fileb://$(ZIPFILE_NAME) --publish

update: deploy

.PHONY: test
test:
	python -W ignore -m unittest test_lambda
