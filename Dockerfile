FROM python:3.8.1-alpine
RUN apk add --no-cache postgresql-dev build-base
RUN python3 -m pip install virtualenv
RUN virtualenv venv -p python3.8.1
COPY . .
RUN . venv/bin/activate && pip install -r requirements.txt
CMD . venv/bin/activate && python manage.py run