# STAGE 1: Exporting requirements.txt
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock* ./

RUN poetry lock
# Export requirements.txt from poetry
RUN poetry self add poetry-plugin-export && \
    poetry export -f requirements.txt --without-hashes --output requirements.txt


# STAGE 2: Building final image for lambda
FROM public.ecr.aws/lambda/python:3.12

WORKDIR /var/task

COPY --from=builder /app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt --target /var/task

COPY . .

ENV PYTHONPATH="/var/task:$PYTHONPATH"

# Lambda entrypoint
CMD ["main.lambda_handler"]

