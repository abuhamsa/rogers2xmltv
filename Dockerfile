FROM ubuntu


# Set workdir and add pythonscript
WORKDIR /app
ADD /app ./

COPY cron/rogers2xmltv.cron /etc/rogers2xmltv.cron
COPY init/entrypoint /usr/local/sbin/entrypoint

# Volumes
VOLUME /data

# Update Timezonedoc
ENV TZ=Europe/Zurich
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Env
ENV USE_STATIC_CHANNELS=yes \
    DATE_RANGE=21 \
    CHANNEL_SOURCE=rog_ott_sdh_ch \
    ICON="https://picon-13398.kxcdn.com/rogersca.jpg"

# RUN
RUN apt-get update -qy \
### install basic packages
&& apt-get install -qy python3-pip tzdata cron python-is-python3\
### rogers2xmltv Stuff
&& chmod +x /usr/local/sbin/entrypoint \  
&& chmod 644 /etc/rogers2xmltv.cron \
&& umask 022

# Install pip depenencies
RUN pip3 install requests pytz

#CMD [ "python", "main.py" ] 
ENTRYPOINT [ "/usr/local/sbin/entrypoint" ]