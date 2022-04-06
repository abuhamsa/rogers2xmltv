# rogers2xmltv - convert rogers api to xmltv

This python-tool provides a simple solution to get a schedule for the rogers [super sports pak](https://supersportspak.com/) and convert it to the [xmltv-format](http://wiki.xmltv.org/index.php/XMLTVFormat).

## Run
```
docker run \
-d \
-e FREQUENCY="0 2 * * *" \
-e DATE_RANGE="21" \
-e ICON="https://picon-13398.kxcdn.com/rogersca.jpg" \
-e CHANNEL_SOURCE="rog_ott_sdh_ch" \
-e USE_STATIC_CHANNELS="yes" \
-v /mnt/user/appdata/rogers2xmltv:/data:rw \
--name=rogers2xmltv \
rogers2xmltv:latest
```
## Setup
### Environment Variables
You can change the some defaults be setting environment variables.
`sample.env` should be renamed to `.env` and supplied through the `--env-file` docker run option. The `.env` file can also be picked up if using this in a `docker compose` setup.

### Cronjob
The default schedule for the cronjob is set to 02:00:00 AM.
You can change the frequency by setting the FREQUENCY-Environment variable

### Run the script manually
NOT IMPLEMENTED YET
Simply run the cronjob file inside the Docker container  
`docker exec rogers2xmltv python /app/main.py`