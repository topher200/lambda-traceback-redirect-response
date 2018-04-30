"""
    Redirect any requests for a traceback to its Kibana page.

    Why are we using this level of indirection instead of just making links straight to Kibana?
    Answer: Kibana's github explicitly says that they reserve the abilitiy to change their URL
    scheme in the future. If they ever do (or if we build our own tracebacks viewer), we want any
    links that we've made in Jira to continue working.

    So all external links to tracebacks (ie: jira) will point to this server, and this server will
    stay updated with the URL of Kibana or FutureViewerX.
"""

import datetime

import requests

from chalice import Chalice, Response


ES_ADDRESS = 'https://stats-from-logs.wordstream-sandbox.com'

GET_TRACEBACK_FROM_ES_TEMPALTE = '{es_address}/traceback-index/traceback/{papertrail_id}'

ARCHIVE_LINK_TEMPLATE = (
    "{kibana_address}/_plugin/kibana/app/kibana#"
    "/doc/c9685a80-12b5-11e8-bd6d-e15cb8d01613/"
    "traceback-index/traceback?id={papertrail_id}"
)
"""
    A template for linking to a papertrail object archive.

    Caller must provide:
    - a link to the kibana domain, no trailing slash. example: 'https://kibana.company.com'
    - the papertrail id to highlight on. example: '926890000000000000'
"""

PAPERTRAIL_LINK_TEMPLATE = (
    'https://papertrailapp.com/systems/{instance_id}/events?focus={papertrail_id}'
)
"""
    A template for linking directly to papertrail

    Caller must provide:
    - the papertrail id to highlight on. example: '926890000000000000'
    - the instance id of the log message. example: 'i-XXXXXXXXXX'
"""


app = Chalice(app_name='lambda-traceback-redirect-response')
app.debug = True


# if anyone requests a traceback, send a redirect
@app.route('/traceback/{papertrail_id}')
def traceback(papertrail_id):
    date_, instance_id = __get_traceback_metadata(papertrail_id)
    thirty_days_ago = datetime.date.today() - datetime.timedelta(days=30)
    if date_ < thirty_days_ago:
        print('date %s too old for papertrail' % date_)
        url = ARCHIVE_LINK_TEMPLATE.format(
            kibana_address=ES_ADDRESS,
            papertrail_id=papertrail_id,
        )
    else:
        print('date %s is young enough for papertrail' % date_)
        url = PAPERTRAIL_LINK_TEMPLATE.format(
            papertrail_id=papertrail_id,
            instance_id=instance_id,
        )

    return Response(
        status_code=302,
        body='',
        headers={'Location': url}
    )


def __get_traceback_metadata(papertrail_id):
    """
        asks Elasticsearch for metadata around the given traceback.

        Returns a two-tuple of the following data:
        - date of the traceback
        - instance id of the server who created the traceback
    """
    # get traceback from elasticsearch
    res = requests.get(GET_TRACEBACK_FROM_ES_TEMPALTE.format(
        es_address=ES_ADDRESS, papertrail_id=papertrail_id
    ))
    try:
        traceback_dict = res.json()
    except Exception:
        print('failed to parse ES response')
        raise

    # get timestamp string
    try:
        datetime_str = traceback_dict['_source']['origin_timestamp']
    except Exception:
        print('failed to get origin_timestamp from response')
        print('json: "%s"' % traceback_dict)
        raise

    # parse datetime string into python date
    # 2018-04-24T06:08:59-0400 -> datetime.datetime(2018, 4, 24, 0, 0)
    try:
        date_str = datetime_str.split('T')[0]
        date_ = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except Exception:
        print('failed to parse date from timestamp. ts: %s' % datetime_str)
        raise

    # get instance id
    try:
        instance_id = traceback_dict['_source']['instance_id']
    except Exception:
        print('failed to get instance_id from response')
        print('json: "%s"' % traceback_dict)
        raise

    return (date_, instance_id)


# just for debugging
@app.route('/')
def index():
    return {'hello': 'world'}
