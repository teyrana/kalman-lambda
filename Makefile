ACCOUNT_ID = --YOUR ACCOUNT ID
ROLE_NAME = --ROLE NAME YOUR FUNCTION WILL USE
FUNCTION_NAME = --FUNCTION NAME
REGION = --REGION ex. us-east-1
TIMEOUT = --TIMEOUT ex. 15
MEMORY_SIZE = --MEMORY SIZE ex. 192
ZIPFILE_NAME = --NAME OF THE ZIPPED FUNCTION
HANDLER = --FILE WITH HANDLER FUNCTION ex. lambda-code.lambda_handler

clean_pyc :
	find . | grep .pyc$ | xargs rm

install_deps :
	pip install -r requirements.txt -t libs/

build : install_deps clean_pyc
	zip $(ZIPFILE_NAME) -r *

create : build
	aws lambda create-function --region $(REGION) --function-name $(FUNCTION_NAME) --zip-file fileb://$(ZIPFILE_NAME) --role arn:aws:iam::$(ACCOUNT_ID):role/$(ROLE_NAME)  --handler $(HANDLER) --runtime python2.7 --timeout $(TIMEOUT) --memory-size $(MEMORY_SIZE)

update : build
	aws lambda update-function-code --region $(REGION) --function-name $(FUNCTION_NAME) --zip-file fileb://$(ZIPFILE_NAME) --publish