FROM node:20-alpine as zimui

WORKDIR /src
COPY zimui /src
RUN yarn install --frozen-lockfile
RUN yarn build


FROM python:3.11.4-bookworm
LABEL org.opencontainers.image.source https://github.com/openzim/freecodecamp

RUN python -m pip install --no-cache-dir -U \
      pip

# Copy code + associated artifacts + zimui build output
COPY LICENSE LICENSE.fcc.md README.md /src/
COPY scraper/pyproject.toml scraper/tasks.py /src/scraper/
COPY scraper/src /src/scraper/src
COPY --from=zimui /src/dist /src/zimui

# Install + cleanup
RUN pip install --no-cache-dir /src/scraper \
 && rm -rf /src/scraper

# default output directory
RUN mkdir -p /output
WORKDIR /output

ENTRYPOINT ["fcc2zim"]
