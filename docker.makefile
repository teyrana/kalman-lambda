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
	rm -f $(ZIPFILE_NAME)

install_deps : clean
	pip install --upgrade -r requirements.txt -t libs/

build : install_deps
	rm -rf libs/*-info
	rm -rf libs/numpy/lib/tests/
	#rm -rf libs/numpy/test*
	rm -rf `find libs/scipy/ -regex ".*test.*"`
	rm -rf `find libs/pykalman/ -regex ".*test.*"`
	rm -rf libs/scipy/*.txt
	rm -rf libs/scipy/cluster/
	rm -rf libs/scipy/f2py/
	rm -rf libs/scipy/fftpack/
	rm -rf libs/scipy/integrate/
	rm -rf libs/scipy/io/
	rm -rf libs/scipy/interpolate/
	rm -rf libs/scipy/ndimage/
	rm -rf libs/scipy/sparse/
	rm -rf libs/scipy/spatial/
	rm -rf libs/scipy/stats/
	rm -rf libs/scipy/optimize
	zip $(ZIPFILE_NAME) -r *

$(ZIPFILE_NAME): build

configure: $(ZIPFILE_NAME)
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
