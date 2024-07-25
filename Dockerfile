FROM python:3.12

WORKDIR /archweb

COPY requirements.txt .

COPY requirements_prod.txt .

RUN pip install --no-cache-dir -r requirements_prod.txt

COPY . .

CMD ["python", "manage.py", "collectstatic", "--noinput"]

CMD ["python", "manage.py", "migrate"]

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
