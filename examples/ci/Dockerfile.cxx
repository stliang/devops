FROM container_registery.my_company.com:5004/ubuntu:20.04

ENV PATH="/usr/lib/ccache:${PATH}" \
    KERNEL_VERSION=5.4.0-65-generic \
    TZ=America/Los_Angeles

# This is needed for the following apt-get
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

## Install tools needed to build and run application
RUN apt-get update && apt-get install -y \
    apt-utils \
    build-essential \
    ccache \
    cmake \
    curl \
    default-jdk \
    git \
    jq \
    python3-pip \
    ruby-dev \
    wget

RUN gem install --version 1.11.0 fpm
RUN pip install gcovr ipython

## Install application test and metrics tools

WORKDIR /opt

# Download googletest
RUN git clone -b release-1.12.1 https://github.com/google/googletest.git

# Download mend's unified agent
RUN wget -q https://unified-agent.s3.amazonaws.com/wss-unified-agent.jar

# Build googletest
WORKDIR /opt/googletest/build
RUN cmake .. \
 && make install

# Download sonar build-wrapper
ENV SONAR_WRAPPER_FILE=build-wrapper-linux-x86.zip
RUN curl -OL https://sonarqube.my_company.com/static/cpp/$SONAR_WRAPPER_FILE \
    && unzip -q $SONAR_WRAPPER_FILE -d / \
    && rm -f $SONAR_WRAPPER_FILE

# Download sonar-scanner
ENV ARTIFACTORY=http://container_registery.my_company.com:8081/artifactory
ENV SONAR_SCANNER_FILE=sonar-scanner-cli-4.6.2.2472-linux.zip
RUN wget -q $ARTIFACTORY/Files/sonar-scanner/$SONAR_SCANNER_FILE \
    && unzip -q $SONAR_SCANNER_FILE -d / \
    && rm -f $SONAR_SCANNER_FILE

WORKDIR /home/jenkins
