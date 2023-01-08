FROM python:3.10
WORKDIR /api

RUN echo "Starting backend build..."

RUN pip install pipenv

COPY  . .

RUN pipenv install --system --deploy --ignore-pipfile

ENV FLASK_ENV production

CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5001", "wsgi:app", "--timeout", "90"]