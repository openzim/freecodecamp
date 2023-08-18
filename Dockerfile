FROM mcr.microsoft.com/devcontainers/typescript-node:20 as client

WORKDIR /src
COPY client /src
RUN yarn install --frozen-lockfile
RUN yarn build


FROM python:3.11-buster

WORKDIR /src
COPY openzim/requirements.pip /src
RUN pip install -r requirements.pip --no-cache-dir

COPY openzim /src
COPY --from=client /src /src/client


ENTRYPOINT ["python3", "fcctozim"]