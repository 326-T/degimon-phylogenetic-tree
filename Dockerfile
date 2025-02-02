FROM python:3.12 AS base
RUN apt-get update && apt-get install -y \
    graphviz \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*
RUN useradd -m fastapi

FROM base AS deps
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

FROM deps AS runner
COPY --chown=fastapi:fastapi ./app /code/app
COPY --chown=fastapi:fastapi ./static /code/static
COPY --chown=fastapi:fastapi ./templates /code/templates

USER fastapi

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]