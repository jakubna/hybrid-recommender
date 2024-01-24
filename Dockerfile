FROM python:3.10-slim

WORKDIR /home/rsapp

COPY requirements.txt requirements.txt

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --upgrade pip --no-cache-dir
RUN pip install -r requirements.txt --no-cache-dir
RUN pip install gunicorn cryptography

COPY main.py examples.py db.json constant.py run.sh ./
RUN chmod +x run.sh

EXPOSE 8020

ENTRYPOINT ["./run.sh"]
CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:8020", "main:app"]