FROM ubuntu


# Set workdir and add pythonscript
WORKDIR /app
ADD /app ./

COPY init/entrypoint /usr/local/sbin/entrypoint
COPY cron/cronjob.sh /cronjob.sh


# Volumes
VOLUME /data

# Update Timezonedoc
ENV TZ=Europe/Zurich
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Env
ENV USE_STATIC_CHANNELS=yes \
    DATE_RANGE=21 \
    CHANNEL_SOURCE=rog_ott_sdh_ch \
    ICON=https://picon-13398.kxcdn.com/rogersca.jpg \
    use_xTeveAPI=no\
    xteveURL= \
    use_plexAPI=no \
    plexUpdateURL=



# RUN
RUN apt-get update -y \
### install basic packages
&& apt-get install -qy python3-pip tzdata cron python-is-python3 curl nano\
&& which cron \
&& rm -rf /etc/cron.*/* \
### rogers2xmltv Stuff
&& chmod +x /usr/local/sbin/entrypoint \
&& chmod +x /cronjob.sh

# Install pip depenencies
RUN pip3 install requests pytz

COPY cron/rogers2xmltv_base.cron /etc/crontab

ENTRYPOINT [ "/usr/local/sbin/entrypoint" ]
CMD ["cron","-f", "-l", "2"]