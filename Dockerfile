FROM python:3.6
# Set PYTHONUNBUFFERED so output is displayed in the Docker log
# if this would use django/flask and expose end points..
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /usr/src/app
RUN  python /usr/src/app/setup.py install
ENTRYPOINT [ "./run_app.sh" ]