# rogers2xmltv - convert rogers api to xmltv

This python-tool provides a simple solution to get a schedule for the rogers [super sports pak](https://supersportspak.com/) and convert it to the [xmltv-format](http://wiki.xmltv.org/index.php/XMLTVFormat).

## Run
```
docker run -d \
	--name=xteve_lazystream \
	-p 34400:34400 \
	-e TZ="America/Los_Angeles" \
	--env-file=.env \
	--log-opt max-size=10m \
	--log-opt max-file=3 \
	-v /mnt/user/appdata/xteve/.xteve:/xteve:rw \
	-v /mnt/user/appdata/xteve/config/:/config:rw \
	-v /mnt/user/appdata/xteve/guide2go/:/guide2go:rw \
	-v /mnt/user/appdata/xteve/playlists/:/playlists:rw \
	-v /tmp/xteve/:/tmp/xteve:rw \
	taylorbourne/xteve_lazystream
```
## Setup
### Environment Variables
You can change the some defaults be setting environment variables.
`sample.env` should be renamed to `.env` and supplied through the `--env-file` docker run option. The `.env` file can also be picked up if using this in a `docker compose` setup.

### Cronjob
The default schedule for the cronjob is set to run every hour.
You can set your own schedule by renaming the `sample_cron.txt` file in the `/config` volume to `cron.txt` and editing the schedule. Make sure to restart your container to take effect.

#### Testing cronjob function

Simply run the cronjob file inside the Docker container  
`docker exec -it dockername ./cronjob.sh`
