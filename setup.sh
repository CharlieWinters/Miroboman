#!/bin/zsh

### This is a setup script to be used when testing Miroboman locally.
### Add in values for JIRA_AUTH, JIRA_BASE_URL, JIRA_PROJECT_KEY, MIRO_AUTH
### You may need to give permission to run the command with 'chmod +x ./setup.sh'
### Run this script with 'source setup.sh'


export ENVIRONMENT=''
# set to LOCAL when testing locally

export JIRA_AUTH=''
# set the jira access token

export JIRA_BASE_URL=''
# set the jira base url

export JIRA_PROJECT_KEY=''
# set the jira project key

export JIRA_SUBTASK_ID=''
# set the subtask if for the Jira project
# 10003 for miro-tests.atlassian
# 10007 for miro.atlassian

export MIRO_AUTH=''
# set the MIRO auth 

PYTHON=$(which python3)
# Set python interpreter you want for your environment

PIP=$(which pip3)
# Set pip interpreter you want for your environment

$PIP install virtualenv
# Install virtualenv

$PYTHON -m venv env
# Create you virtual environment

source ./env/bin/activate
# activate virtual environment

$PIP install -r requirements.txt
# install required packages