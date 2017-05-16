FROM ubuntu:latest
MAINTAINER geonaut "geonaut@geonaut.co.uk"
RUN apt-get update -y
RUN apt-get install -y python-pip curl python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN nosetests tests/unit_tests.py --with-coverage --cover-package=app
ENTRYPOINT ["python"]
CMD ["app.py"]