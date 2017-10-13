import sys

from pathlib import Path

# Munge our sys path so libs can be found
CWD = Path(__file__).resolve().cwd() / 'lib'
sys.path.insert(0, str(CWD))

import simplejson as json

from cupping.handlers.session import (
        handle_session,
        handle_session_detail,
)
from cupping.exceptions import Http404


def session(event, context):
    """/session endpoint for POST or GET"""
    http_method = event['httpMethod']

    status_code = 200
    response = {}

    try:
        response = handle_session(http_method, event)
    except Exception as e:
        status_code = 500
        # TODO - log error
        response = {'errors': ['Unexpected server error']}

    response = {
        'statusCode': status_code,
        'body': json.dumps(response)
    }

    return response


def session_detail(event, context):
    http_method = event['httpMethod']

    status_code = 200
    response = {}

    try:
        response = handle_session_detail(http_method, event)
    except Http404 as e:
        status_code = 404
        response = {'errors': [str(e)]}
    except Exception as e:
        status_code = 500
        # TODO - log error
        response = {'errors': ['Unexpected server error']}

    response = {
        'statusCode': status_code,
        'body': json.dumps(response)
    }

    return response


if __name__ == '__main__':
    with open ('../create-new-session-missing-data.json', 'r') as fh:
        event = json.loads(fh.read())
        session(event, None)
