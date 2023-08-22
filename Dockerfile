FROM mcr.microsoft.com/devcontainers/typescript-node:20 as zimui

WORKDIR /src
COPY zimui /src
RUN yarn install --frozen-lockfile
RUN yarn build


FROM python:3.11.4-bookworm
LABEL org.opencontainers.image.source https://github.com/openzim/freecodecamp

WORKDIR /src
COPY scraper/requirements.txt /src
RUN pip install -r requirements.txt --no-cache-dir

COPY scraper /src
COPY --from=zimui /src/dist /src/zimui

WORKDIR /output

ENTRYPOINT ["python3", "/src/fcc2zim"]