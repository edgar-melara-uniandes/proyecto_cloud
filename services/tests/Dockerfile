FROM python:3.10.2-slim-buster
RUN pip install bzt
RUN apt-get update && apt-get -y install default-jre-headless
RUN bzt -install-tools -o modules.install-checker.include=jmeter
ENTRYPOINT ["bzt"]