FROM python:3.10-alpine

WORKDIR /app

RUN pip install poetry==1.7.0

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root

COPY kube_cleaner/ kube_cleaner/

ENTRYPOINT [ "poetry", "run" ,"kopf", "run", "kube_cleaner/cleanup_policies.py" ]