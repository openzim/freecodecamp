FROM node:26-alpine AS zimui

# Node 25+ images do not ship corepack anymore
RUN npm install -g corepack && corepack enable

WORKDIR /src
COPY zimui /src/zimui
WORKDIR /src/zimui
RUN yarn install --immutable
RUN yarn build


FROM python:3.14-trixie
LABEL org.opencontainers.image.source=https://github.com/openzim/freecodecamp

RUN python -m pip install --no-cache-dir -U \
      pip

# Copy code + associated artifacts
COPY LICENSE LICENSE.fcc.md README.md /src/
COPY scraper/pyproject.toml scraper/openzim.toml scraper/tasks.py /src/scraper/
COPY scraper/src /src/scraper/src

# Copy zimui build output
COPY --from=zimui /src/scraper/src/fcc2zim/zimui /src/scraper/src/fcc2zim/zimui

# Install + cleanup
RUN pip install --no-cache-dir /src/scraper \
 && rm -rf /src/scraper

# default output directory
RUN mkdir -p /output
WORKDIR /output

ENV FCC_BUILD=/tmp
ENV FCC_OUTPUT=/output

CMD ["fcc2zim", "--help"]
