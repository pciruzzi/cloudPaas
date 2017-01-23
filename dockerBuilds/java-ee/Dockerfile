FROM ubuntu:14.04

# Install node & npm
RUN apt-get -q update && apt-get -q -y install vim git nodejs npm nano
RUN ln -s /usr/bin/nodejs /usr/bin/node
# Install Wetty
WORKDIR /opt/wetty
RUN git clone https://github.com/krishnasrinivas/wetty.git . && git reset --hard 223b1b1
RUN npm install
EXPOSE 3000
# Install everything related to this type of container
RUN apt-get -q -y install curl
RUN apt-get -q -y install software-properties-common
RUN \
  echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections && \
  add-apt-repository -y ppa:webupd8team/java && \
  apt-get update && \
  apt-get install -y oracle-java8-installer && \
  rm -rf /var/lib/apt/lists/* && \
  rm -rf /var/cache/oracle-jdk8-installer
RUN apt-get update
RUN wget --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/java_ee_sdk/7u3/java_ee_sdk-7u2.zip
RUN apt-get -q -y install unzip
RUN unzip java_ee_sdk-7u2.zip
# TODO: Complete!!
# Set-up term user and run web-terminal
CMD if [ ! "$(getent passwd $DOCKER_USER)" ] ; then useradd -d /home/$DOCKER_USER -m -s /bin/bash $DOCKER_USER && echo "$DOCKER_USER:$DOCKER_PASS" | chpasswd && env | grep -v '^HOME\|^PWD\|^PATH' | while read env; do echo "export $env" >> /home/$DOCKER_USER/.bashrc ; done ; fi && node /opt/wetty/app.js -p 3000
