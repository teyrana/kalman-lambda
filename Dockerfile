# Forked from:
# git@github.com:lambci/docker-lambda.git

FROM lambci/lambda:build-python3.6

ENV LANG=en_US.UTF-8 \
    AWS_EXECUTION_ENV=AWS_Lambda_python3.6 \
    PYTHONPATH=/var/runtime

COPY requirements.txt ./
RUN pip install --upgrade -r requirements.txt -t libs/

COPY env.makefile ./

COPY ./docker.makefile ./Makefile
RUN touch Makefile

# finally, install our project into the container
# ... BUT NOT our dependencies
COPY lambda_code.py lambda.json test_lambda.py requirements.txt ./

# Run this make command when the container launches
CMD ["make", "deploy"]
