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
# Set-up term user and run web-terminal
CMD if [ ! "$(getent passwd $DOCKER_USER)" ] ; then useradd -d /home/$DOCKER_USER -m -s /bin/bash $DOCKER_USER && echo "$DOCKER_USER:$DOCKER_PASS" | chpasswd && env | grep -v '^HOME\|^PWD\|^PATH' | while read env; do echo "export $env" >> /home/$DOCKER_USER/.bashrc ; done ; fi && node /opt/wetty/app.js -p 3000
