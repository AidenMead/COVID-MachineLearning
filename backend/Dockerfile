FROM python:3.10
WORKDIR /api

RUN echo "Starting backend build..."

RUN pip install pipenv

COPY  . .

RUN pipenv install --system --deploy --ignore-pipfile

ENV FLASK_ENV production

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "app:app", "--timeout", "600"]