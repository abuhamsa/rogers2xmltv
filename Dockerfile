FROM python:3

# Install pip depenencies
RUN pip install requests pytz

# Set workdir and add pythonscript
WORKDIR /app
ADD main.py ./


# Volumes
VOLUME /data

# Update Timezone
ENV TZ=Europe/Zurich
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Env
ENV use_static_channels=yes \
    date_range=21 \
    channel_source=rog_ott_sdh_ch \
    icon="https://picon-13398.kxcdn.com/rogersca.jpg"


CMD [ "python", "main.py" ] 