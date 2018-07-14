Redirect any requests for a traceback to its Kibana page.

Why are we using this level of indirection instead of just making links straight to Kibana?
Answer: Kibana's github explicitly says that they reserve the abilitiy to change their URL
scheme in the future. If they ever do (or if we build our own tracebacks viewer), we want any
links that we've made in Jira to continue working.

So all external links to tracebacks (ie: jira) will point to this server, and this server will
stay updated with the URL of Kibana or FutureViewerX.

## Deploy

See Makefile for options.

To deploy...
- run `make` to deploy
- you need to manually put the lambda function into the Sandbox VPC and give it the stats-from-logs Security Group
- provide the env variable ES_ADDRESS (example: https://es_address.company-sandbox.com)

