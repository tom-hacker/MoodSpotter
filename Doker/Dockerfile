FROM java:openjdk-8-jdk
ENV JAVA_OPTS="-Djava.net.preferIPv4Stack=true -Djava.net.preferIPv4Addresses=true"

ADD thorntail.jar /opt/thorntail.jar

EXPOSE 8082
ENTRYPOINT exec java $JAVA_OPTS -jar /opt/thorntail.jar