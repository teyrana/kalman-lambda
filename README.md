Lambda Python Boilerplate
========
A basic package with files needed to develop AWS Lambda functions using python.


# Initialization

The makefile and and development expect an existing virtualenv based on 3.6
(But may very well work without it.)

The authors used: 'pyenv' + 'pyenv-virtualenv'

# Requirements:
- Python 3.6 (i.e. the version 3.x supported by Amazon Lambda)
- pip (used to install...)
  -- pykalman
  -- numpy
  -- scipy
- docker


# Development

1. Code
2. Install require modules
3. Update requirements file: `pip freeze > requirements.txt`


# Deployment

Deploy to lambda function code:

```make deploy```
