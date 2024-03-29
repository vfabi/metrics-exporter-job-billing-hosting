FROM ubuntu:20.04


# Metadata
MAINTAINER Vadim Fabi <vaad.fabi@gmail.com>
ARG TARGETARCH
ARG APP_NAME=metrics-exporter-job-billing-hosting
ARG APP_VERSION=1.0.2
ENV APP_NAME=${APP_NAME}
ENV APP_VERSION=${APP_VERSION}
ENV PYTHONUNBUFFERED=1
## Chrome/Chromedriver
ENV TZ=Europe/Kiev
ENV CHROME_VERSION 112.0.5615.165-1
ENV CHROMEDRIVER_VERSION 112.0.5615.49
ENV CHROMEDRIVER_DIR /opt/chromedriver
ENV PATH $CHROMEDRIVER_DIR:$PATH


# Common
RUN apt-get -y update && \
    apt-get -y install python3-pip git wget xvfb unzip

## Setup Chrome
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/chrome.list
# RUN apt-get -y update && apt-get -y install google-chrome-stable
RUN wget --no-verbose -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}_amd64.deb && \
    apt install -y /tmp/chrome.deb

## Setup Chromedriver
RUN mkdir $CHROMEDRIVER_DIR
RUN wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR

## Cleanup
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    rm -rf $CHROMEDRIVER_DIR/chromedriver_linux64.zip && \
    rm -rf /tmp/chrome.deb

## Apps code
ADD app /app
RUN pip install -r /app/requirements.txt
RUN chmod -R 755 /app


# Entrypoint
WORKDIR /app
CMD ["python3", "./main.py"]
