from chalice import Chalice, Response

app = Chalice(app_name='lambda-traceback-redirect-response')


KIBANA_ADDRESS = 'https://stats-from-logs.wordstream-sandbox.com'

ARCHIVE_TEMPLATE = (
    "{kibana_address}/_plugin/kibana/app/kibana#/discover?"
    "_g=(time:(from:now-50y))&"
    "_a=(query:(language:lucene,query:'{papertrail_id}'))]"
)
"""
    A template for linking to a papertrail object archive.

    Caller must provide:
    - a link to the kibana domain, no trailing slash. example: 'https://kibana.company.com'
    - the papertrail id to highlight on. example: '926890000000000000'
"""


@app.route('/traceback/{papertrail_id}', content_types=['text/plain'])
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
