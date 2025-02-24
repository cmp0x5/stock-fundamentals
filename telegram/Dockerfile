FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN python -m venv /app/venv

RUN /app/venv/bin/pip install --upgrade pip && \
	/app/venv/bin/pip install -r requirements.txt

COPY . /app

ENV PATH="/app/venv/bin:$PATH"

#COPY .env .env

CMD ["python", "main.py"]
