FROM python:3.8.5
WORKDIR /app
ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]