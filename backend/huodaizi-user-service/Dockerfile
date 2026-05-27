FROM eclipse-temurin:17-jre-jammy

ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} app.jar

ENV JAVA_OPTS="-Xms512m -Xmx1024m -XX:+UseG1GC -XX:MaxGCPauseMillis=200"
ENV SPRING_PROFILES_ACTIVE=prod

EXPOSE 8001

ENTRYPOINT exec java $JAVA_OPTS -jar /app.jar
