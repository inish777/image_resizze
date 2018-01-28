FROM python:3.6.0

WORKDIR /usr/src/image_resize

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

RUN python manage.py collectstatic
CMD [ "./manage.py", "runserver", "0.0.0.0:8000" ]
