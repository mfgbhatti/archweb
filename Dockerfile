FROM python:3.12

WORKDIR /archweb

COPY requirements.txt .

COPY requirements_prod.txt .

RUN apt update && \
    apt install -y \
    vim \
    memcached && \
    pip install --no-cache-dir -r requirements_prod.txt

COPY . .

ENTRYPOINT ["memcached", "-u", "memcached", "-m", "64", "-c", "1024", "-l", "127.0.0.1,::1", "-o", "modern,drop_privileges"]

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

