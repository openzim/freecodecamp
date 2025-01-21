FROM node:22-alpine AS zimui

WORKDIR /src
COPY zimui /src
RUN yarn install --frozen-lockfile
RUN yarn build


FROM python:3.13.1-bookworm
LABEL org.opencontainers.image.source=https://github.com/openzim/freecodecamp

RUN python -m pip install --no-cache-dir -U \
      pip

# Copy code + associated artifacts + zimui build output
COPY LICENSE LICENSE.fcc.md README.md /src/
COPY scraper/pyproject.toml scraper/openzim.toml scraper/tasks.py /src/scraper/
COPY scraper/src /src/scraper/src
COPY --from=zimui /src/dist /src/zimui

# Install + cleanup
RUN pip install --no-cache-dir /src/scraper \
 && rm -rf /src/scraper

# default output directory
RUN mkdir -p /output
WORKDIR /output

ENV FCC_BUILD=/tmp
ENV FCC_OUTPUT=/output
ENV FCC_ZIMUI_DIST=/src/zimui

CMD ["fcc2zim", "--help"]
