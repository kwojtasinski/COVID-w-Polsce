FROM python:3.11-buster

RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

WORKDIR /app 

COPY pyproject.toml poetry.lock app.py ./

RUN poetry install --without dev --no-cache --no-root

COPY covid_w_polsce ./covid-w-polsce

EXPOSE 8501

CMD ["poetry", "run", "streamlit", "run", "app.py"]