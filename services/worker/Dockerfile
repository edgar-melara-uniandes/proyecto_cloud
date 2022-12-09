FROM gcr.io/google_appengine/python
#RUN apt-get -y update && apt-get install -y --no-install-recommends ffmpeg    para version liviana
RUN apt-get -y update && apt-get install -y ffmpeg

RUN virtualenv /env -p python3.7

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ADD . /app

CMD python3 -m tasks.music_task.py