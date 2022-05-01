FROM ubuntu:focal

# Update Timezone
ENV TZ='Europe/Zurich'
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# ENV for Python App
ENV USE_STATIC_CHANNELS=True
ENV DATE_RANGE=21
ENV CHANNEL_SOURCE=rog_ott_sdh_ch
ENV ICON=https://picon-13398.kxcdn.com/rogersca.jpg
ENV DOCKER_MODE=True
ENV API_MODE=False
ENV URL=https://rogerstv.com/api/ssp?f=schedule

# ENV for Bash Script
ENV USE_XTEVEAPI=False
ENV XTEVEURL=
ENV USE_PLEXAPI=False
ENV PLEXUPDATEURL=

# RUN
RUN apt-get update -y \
### install basic packages
&& apt-get install -qy python3-pip tzdata cron python-is-python3 curl nano
# Setup cron
RUN which cron \
&& rm -rf /etc/cron.*/* 

# Install pip depenencies
RUN pip3 install pytz fastapi uvicorn[standard]

# 1. Install latest Python
RUN apt-get update && apt-get install -y curl unixodbc-dev

# 2. Install WebKit dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libwoff1 \
    libopus0 \
    libwebp6 \
    libwebpdemux2 \
    libenchant1c2a \
    libgudev-1.0-0 \
    libsecret-1-0 \
    libhyphen0 \
    libgdk-pixbuf2.0-0 \
    libegl1 \
    libnotify4 \
    libxslt1.1 \
    libevent-2.1-7 \
    libgles2 \
    libxcomposite1 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libepoxy0 \
    libgtk-3-0 \
    libharfbuzz-icu0

# 3. Install gstreamer and plugins to support video playback in WebKit.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgstreamer-gl1.0-0 \
    libgstreamer-plugins-bad1.0-0 \
    gstreamer1.0-plugins-good \
    gstreamer1.0-libav

# 4. Install Chromium dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 \
    libxss1 \
    libasound2 \
    fonts-noto-color-emoji \
    libxtst6

# 5. Install Firefox dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libdbus-glib-1-2 \
    libxt6

# 6. Install ffmpeg to bring in audio and video codecs necessary for playing videos in Firefox.
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg

# 7. (Optional) Install XVFB if there's a need to run browsers in headful mode
RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb

# 8. Feature-parity with node.js base images.
RUN apt-get update && apt-get install -y --no-install-recommends git ssh

# 9. Install the Microsoft ODBC driver for SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update -y \
    && ACCEPT_EULA=Y apt-get install msodbcsql17 -y \
    && ACCEPT_EULA=Y apt-get install mssql-tools -y \
    && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile \
    && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

#10. Install playwright and pip dependencies
RUN pip install playwright pyodbc PyPDF2 requests bs4 pycryptodome pandas lxml \
    && playwright install    



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