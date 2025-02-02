FROM python:3.12 AS base
RUN apt-get update && apt-get install -y \
    graphviz \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

FROM base AS deps
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

FROM deps AS runner
COPY ./app /code/app
COPY ./static /code/static
COPY ./templates /code/templates

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]