FROM python:3.12

COPY requirments.txt requirments.txt
RUN python -m pip install --upgrade pip && pip install -r requirments.txt

COPY back /mycode/back
EXPOSE 8000
WORKDIR /mycode/back
CMD ["uwsgi", "--http", "0.0.0.0:8000", "--module", "back.wsgi", "--master", "--processes", "4", "--threads", "1"]