FROM library/python:3.9-buster

COPY requirements.txt /

RUN pip install -r /requirements.txt

RUN mkdir /app
COPY src /app/

ENTRYPOINT ["python3", "/app/ransomwatch.py"]
# CMD ["--delay", "3600"]

