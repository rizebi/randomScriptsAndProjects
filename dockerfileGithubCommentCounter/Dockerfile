FROM centos:centos7

RUN yum -y update; yum install -y wget unzip java-1.8.0-openjdk; yum clean all

COPY install.sh /tmp/

RUN chmod +x /tmp/install.sh; /tmp/install.sh

EXPOSE 8080 8081

ENV JAVA_HOME /usr/lib/jvm/jre

RUN export JAVA_HOME

CMD /application/bin/leaderboard-server server /application/config/leaderboard-server.yml