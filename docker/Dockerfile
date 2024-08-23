FROM python:3.10.6 as base

ENV C_FORCE_ROOT=True
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code

WORKDIR /code

RUN /usr/local/bin/python -m pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir poetry==1.3.2

COPY pyproject.toml poetry.lock /code/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --with dev \
    && echo yes | poetry cache clear . --all

COPY scripts/web/startup.sh /scripts/web/startup.sh
RUN chmod u+x /scripts/web/startup.sh

CMD ["/scripts/web/startup.sh", "-m", "-l"]