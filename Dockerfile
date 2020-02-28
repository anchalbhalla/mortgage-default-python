FROM python:3.6

# Create app directory
COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

# Bundle app source
COPY static_app /app

EXPOSE 8080
CMD ["python","app.py"]
