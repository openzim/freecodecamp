FROM node:20-alpine as zimui

WORKDIR /src
COPY zimui /src
RUN yarn install --frozen-lockfile
RUN yarn build


FROM python:3.11.4-bookworm
LABEL org.opencontainers.image.source https://github.com/openzim/freecodecamp

RUN python -m pip install --no-cache-dir -U \
      pip \
      pip-tools

# Copy pyproject.toml and its dependencies and install Python dependencies
# This is separated to benefit from Docker build cache when only
# zimui or Python source code is modified (which is quite often the case)
COPY scraper/src/fcc2zim/__about__.py /src/scraper/src/fcc2zim/__about__.py
COPY scraper/pyproject.toml scraper/pypi-readme.rst /src/scraper/
RUN pip-compile --strip-extras -o requirements.txt /src/scraper/pyproject.toml \
 && pip install --no-cache-dir -r requirements.txt \
 && rm requirements.txt

# Copy zimui build output
COPY --from=zimui /src/dist /src/zimui

# Copy scraper and install it
COPY scraper/src /src/scraper/src
COPY scraper/*.md scraper/*.rst LICENSE LICENSE.fcc.md scraper/*.py /src/scraper/
RUN pip install --no-cache-dir /src/scraper \
 && rm -rf /src/scraper

# default output directory
RUN mkdir -p /output
WORKDIR /output

ENTRYPOINT ["fcc2zim"]
