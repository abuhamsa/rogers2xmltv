# rogers2xmltv - convert rogers api to xmltv

This python-tool provides a simple solution to get a schedule for the rogers [super sports pak](https://supersportspak.com/) and convert it to the [xmltv-format](http://wiki.xmltv.org/index.php/XMLTVFormat).

## Run
```
docker run -d \
	--name=rogers2xmltv \
	-e TZ="Europe/Zurich" \
	-v /mnt/user/appdata/roger2xmltv:/data:rw \
	abuhamsa/rogers2xmltv:latest
```
## Setup
### Environment Variables
NOT FINISHED YET
You can change the some defaults be setting environment variables.
`sample.env` should be renamed to `.env` and supplied through the `--env-file` docker run option. The `.env` file can also be picked up if using this in a `docker compose` setup.

### Cronjob
NOT IMPLEMENTED YET
The default schedule for the cronjob is set to run every hour.
You can set your own schedule by renaming the `sample_cron.txt` file in the `/config` volume to `cron.txt` and editing the schedule. Make sure to restart your container to take effect.

#### Testing cronjob function
NOT IMPLEMENTED YET
Simply run the cronjob file inside the Docker container  
`docker exec -it dockername ./cronjob.sh`
