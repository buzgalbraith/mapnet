FROM openjdk:17
RUN mkdir /package
WORKDIR /package
COPY logmap ./logmap
COPY logmap/parameters.txt ./parameters.txt
COPY resources ./resources
COPY run.sh ./
RUN mkdir output