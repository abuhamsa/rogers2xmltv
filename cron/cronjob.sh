#!/bin/bash
echo "$(date) - START cronjob"
echo "$(date) - START rogers2xmltv-script"
python /app/main.py
echo "$(date) - END rogers2xmltv-script"

# update xteve via API
if [ "$USE_XTEVEAPI" = true ] || [ "$USE_XTEVEAPI" = True ]; then
	echo "$(date) - START update xteve"
	curl -s -X POST -d '{"cmd":"update.m3u"}' http://$XTEVEURL/api/
	sleep 1
	curl -s -X POST -d '{"cmd":"update.xmltv"}' http://$XTEVEURL/api/
	sleep 1
	curl -s -X POST -d '{"cmd":"update.xepg"}' http://$XTEVEURL/api/
	#create a new line
	echo ""
	echo "$(date) - Wating 30s after xteve-update"
	sleep 30
	echo "$(date) - END update xteve"
fi

# update Plex via API
if [ "$USE_PLEXAPI" = true ] || [ "$USE_PLEXAPI" = True ]; then
	echo "$(date) - START update plex"
	# get protocol
	proto="$(echo $PLEXUPDATEURL | grep :// | sed -e's,^\(.*://\).*,\1,g')"
	# remove the protocol
	url="$(echo ${PLEXUPDATEURL/$proto/})"
	# extract the host
	plexHostPort="$(echo ${url/} | cut -d/ -f1)"
	
	if [ -z "$PLEXUPDATEURL" ]; then
		echo "$(date) - PROBLEM no plex credentials provided"
	else
		curl --location --request POST "$PLEXUPDATEURL" -H "authority: $plexHostPort" -H "content-length: 0" -H "pragma: no-cache" -H "cache-control: no-cache" -H "sec-ch-ua: 'Google Chrome';v='95', 'Chromium';v='95', ';Not A Brand';v='99'" -H "accept: text/plain, */*; q=0.01" -H "x-requested-with: XMLHttpRequest" -H "accept-language: en" -H "sec-ch-ua-mobile: ?0" -H "user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36" -H "sec-ch-ua-platform: 'macOS'" -H "origin: http://$plexHostPort" -H "sec-fetch-site: same-origin" -H "sec-fetch-mode: cors" -H "sec-fetch-dest: empty" -H "referer: http://$plexHostPort/web/index.html"
		sleep 1
	fi
	echo "$(date) - END update plex"
fi
echo "$(date) - END cronjob"