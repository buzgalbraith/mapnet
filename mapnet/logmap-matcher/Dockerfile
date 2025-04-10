FROM openjdk:17-alpine
RUN mkdir /package
WORKDIR /package
COPY mapnet/logmap-matcher/logmap ./logmap
COPY mapnet/logmap-matcher/logmap/parameters.txt ./parameters.txt
COPY resources ./resources

COPY mapnet/logmap-matcher/run.sh ./
RUN mkdir output