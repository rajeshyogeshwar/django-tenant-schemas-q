FROM python:3.8-slim as BASE

ENV PYTHONUNBUFFERED 1

FROM BASE as BUILDER

COPY ./test_project/requirements/base.txt /requirements.txt

RUN apt-get update && apt-get install --no-install-recommends -y build-essential \
  libpq-dev \
  gcc \
  git \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get clean \
  && apt-get autoremove

RUN pip3 install --user -r requirements.txt

FROM BUILDER

COPY --from=BUILDER /root/.local/ /usr/local
COPY ./test_project/app /app

RUN groupadd -r django \
  && useradd -r -g django django \
  && chown -R django:django /app 

WORKDIR /app