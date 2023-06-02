FROM python:3.11-buster

COPY . /src/
WORKDIR /src

RUN make setup

CMD ["openzim/fcc2zim"]