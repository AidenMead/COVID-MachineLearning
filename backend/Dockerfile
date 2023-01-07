FROM python:3.10
WORKDIR /api

RUN echo "Starting backen dbuild..."

RUN pip install pipenv

COPY  . .

RUN pipenv install --system --deploy --ignore-pipfile

ENV FLASK_ENV production

CMD ["gunicorn", "-b", ":5001", "app:app"]