FROM python:3.6.0

RUN mkdir -p /usr/src/image_resize
WORKDIR /usr/src/image_resize

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY image_resize/* /usr/src/image_resize/

CMD [ "./manage.py", "runserver", "0.0.0.0:8000" ]