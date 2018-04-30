"""
    Redirect any requests for a traceback to its Kibana page.

    Why are we using this level of indirection instead of just making links straight to Kibana?
    Answer: Kibana's github explicitly says that they reserve the abilitiy to change their URL
    scheme in the future. If they ever do (or if we build our own tracebacks viewer), we want any
    links that we've made in Jira to continue working.

    So all external links to tracebacks (ie: jira) will point to this server, and this server will
    stay updated with the URL of Kibana or FutureViewerX.
"""

from chalice import Chalice, Response


KIBANA_ADDRESS = 'https://stats-from-logs.wordstream-sandbox.com'

ARCHIVE_TEMPLATE = (
    "{kibana_address/_plugin/kibana/app/kibana#"
    "/doc/c9685a80-12b5-11e8-bd6d-e15cb8d01613/"
    "traceback-index/traceback?id={papertrail_id}"
)
"""
    A template for linking to a papertrail object archive.

    Caller must provide:
    - a link to the kibana domain, no trailing slash. example: 'https://kibana.company.com'
    - the papertrail id to highlight on. example: '926890000000000000'
"""


app = Chalice(app_name='lambda-traceback-redirect-response')
app.debug = True


# if anyone requests a traceback, send a redirect
@app.route('/traceback/{papertrail_id}')
def traceback(papertrail_id):
    url = ARCHIVE_TEMPLATE.format(
        kibana_address=KIBANA_ADDRESS,
        papertrail_id=papertrail_id
    )
    return Response(
        status_code=302,
        body='',
        headers={'Location': url}
    )


# just for debugging
@app.route('/')
def index():
    return {'hello': 'world'}
