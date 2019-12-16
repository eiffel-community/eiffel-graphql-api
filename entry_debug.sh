#!/bin/bash

gunicorn eiffel_graphql_api.wsgi:APP \
	--name eiffel_graphql_api \
	--worker-class=gevent \
	--bind 0.0.0.0:5001 \
	--timeout=300 \
	--worker-connections=1000 \
	--workers=5 \
	--reload
