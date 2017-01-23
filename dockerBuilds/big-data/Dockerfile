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
# RUN apt-get install xxxx # par exemple...
#RUN apt-get -q -y install default-jdk
RUN apt-get -q -y install curl
RUN apt-get -q -y install software-properties-common
# Install Java.
RUN \
  echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections && \
  add-apt-repository -y ppa:webupd8team/java && \
  apt-get update && \
  apt-get install -y oracle-java8-installer && \
  rm -rf /var/lib/apt/lists/* && \
  rm -rf /var/cache/oracle-jdk8-installer
#RUN echo "deb http://www.apache.org/dist/cassandra/debian 22x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
#RUN echo "deb-src http://www.apache.org/dist/cassandra/debian 22x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
#RUN gpg --keyserver pgp.mit.edu --recv-keys F758CE318D77295D
#RUN gpg --export --armor F758CE318D77295D | sudo apt-key add -
#RUN gpg --keyserver pgp.mit.edu --recv-keys 2B5C1B00
#RUN gpg --export --armor 2B5C1B00 | sudo apt-key add -
#RUN gpg --keyserver pgp.mit.edu --recv-keys 0353B12C
#RUN gpg --export --armor 0353B12C | sudo apt-key add -
RUN apt-get update
#RUN curl -L http://debian.datastax.com/debian/repo_key | sudo apt-key add -
#RUN echo "deb http://debian.datastax.com/community stable main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
#RUN apt-get -q -y install dsc30=3.0.2-1 cassandra=3.0.2
#RUN apt-get -q -y install cassandra-tools=3.0.2
RUN apt-key adv --keyserver pgp.mit.edu --recv-keys F758CE318D77295D
RUN echo "deb http://www.apache.org/dist/cassandra/debian 22x main" | tee -a /etc/apt/sources.list.d/cassandra.list
RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe" >> /etc/apt/sources.list
RUN apt-get update && apt-get -y --force-yes install apt-utils cassandra
#RUN apt-get -q -y install cassandra
RUN apt-get -q -y install ssh
RUN apt-get -q -y install rsync

# Hadoop config
RUN addgroup hadoop
RUN adduser --disabled-password --ingroup hadoop --quiet --gecos "" hduser

RUN mkdir -p /home/hduser/.ssh/; mkdir -p /root/.ssh/

# Creating hduser keys (for self ssh login)
RUN ssh-keygen -t rsa -P "" -f /home/hduser/.ssh/id_rsa -C "hduser"
RUN cat /home/hduser/.ssh/id_rsa.pub >> /home/hduser/.ssh/authorized_keys
RUN cat /home/hduser/.ssh/id_rsa.pub >> /home/hduser/.ssh/known_hosts
RUN echo "StrictHostKeyChecking no" >> /home/hduser/.ssh/config
RUN mkdir /var/run/sshd
RUN chmod 0755 /var/run/sshd

# Import master pub key and append it to authorized_keys for no-password login
#ADD keys/master.pub /home/hduser/.ssh/master.pub
#RUN cat /home/hduser/.ssh/master.pub >> /home/hduser/.ssh/authorized_keys
#RUN cat /home/hduser/.ssh/master.pub >> /root/.ssh/authorized_keys


# Owning .ssh
RUN chown -R hduser:hadoop /home/hduser/.ssh/

# Now you can sshd into docker with 'ssh hduser@10.0.10.1 -i keys/master -o StrictHostKeyChecking=no'

# Creating Hadoop folders and setting permissions + temp dir
RUN chown -R hduser:hadoop /usr/local/
RUN mkdir -p /var/local/hadoop/ && chown -R hduser:hadoop /var/local/hadoop/
RUN mkdir -p /app/hadoop/tmp && chown hduser:hadoop /app/hadoop/tmp && chmod 750 /app/hadoop/tmp

RUN apt-get -q -y install python-software-properties
RUN apt-get -q -y update
RUN apt-get -q -y upgrade

# Set-up term user and run web-terminal
CMD if [ ! "$(getent passwd $DOCKER_USER)" ] ; then useradd -d /home/$DOCKER_USER -m -s /bin/bash $DOCKER_USER && echo "$DOCKER_USER:$DOCKER_PASS" | chpasswd && env | grep -v '^HOME\|^PWD\|^PATH' | while read env; do echo "export $env" >> /home/$DOCKER_USER/.bashrc ; done ; fi && node /opt/wetty/app.js -p 3000
