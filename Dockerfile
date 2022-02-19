FROM library/python:3.10-bullseye

COPY requirements.txt /

RUN pip install -r /requirements.txt

RUN playwright install chromium
RUN playwright install-deps chromium

# Some dependencies for playwright/chromium
RUN apt-get install -y \
    libwoff1 libopus0 libwebp6 libwebpdemux2 libenchant-2-2 libgudev-1.0-0 libsecret-1-0 libhyphen0 \
    libgdk-pixbuf2.0-0 libegl1 libnotify4 libxslt1.1 libevent-2.1-7 libgles2 libxcomposite1 libatk1.0-0 \
    libatk-bridge2.0-0 libepoxy0 libgtk-3-0 libharfbuzz-icu0 libnss3 libxss1 libasound2 fonts-noto-color-emoji libxtst6

RUN mkdir /app
COPY src /app/

CMD python3 /app/ransomwatch.py
