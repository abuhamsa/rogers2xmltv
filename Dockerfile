FROM ubuntu



# Update Timezone
ENV TZ=Europe/Zurich
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# ENV for Python App
ENV USE_STATIC_CHANNELS=True \
    DATE_RANGE=21 \
    CHANNEL_SOURCE=rog_ott_sdh_ch \
    ICON=https://picon-13398.kxcdn.com/rogersca.jpg \
    DOCKER_MODE=True \
    API_MODE=False \
    URL=https://rogerstv.com/api/ssp?f=schedule

# ENV for Bash Script
ENV USE_XTEVEAPI=False\
    XTEVEURL= \
    USE_PLEXAPI=False \
    PLEXUPDATEURL=  

# RUN
RUN apt-get update -y \
### install basic packages
&& apt-get install -qy python3-pip tzdata cron python-is-python3 curl nano python3-venv
# Setup cron
RUN which cron \
&& rm -rf /etc/cron.*/* 

RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Install pip depenencies
RUN pip3 install requests pytz lxml fastapi uvicorn[standard] 


# COPY Scripts
COPY cron/cronjob.sh /cronjob.sh
COPY init/entrypoint /usr/local/sbin/entrypoint
# COPY crontab
COPY cron/rogers2xmltv_base.cron /etc/crontab

### Set permissions
RUN chmod +x /usr/local/sbin/entrypoint \
&& chmod +x /cronjob.sh

# Setup WORKDIR and adding python app
WORKDIR /app
ADD /app ./

# Volumes
VOLUME /data

EXPOSE 8000

ENTRYPOINT [ "/usr/local/sbin/entrypoint" ]
CMD ["cron","-f", "-l", "2"]