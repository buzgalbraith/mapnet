FROM openjdk:17-alpine
RUN mkdir /package
WORKDIR /package
COPY logmap ./logmap
COPY logmap/parameters.txt ./parameters.txt
COPY resources ./resources
## probs want to install python, and the package, then add a section that uses the code to download the ontologies and filter mesh for disease.
## could also store in git lfs or something.
# RUN mkdir resources

COPY run.sh ./
RUN mkdir output