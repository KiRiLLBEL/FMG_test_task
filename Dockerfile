FROM python:3.10
WORKDIR /app/

ADD ./requirements.txt /app/requirements.txt
RUN pip install -r ./requirements.txt



ADD . /app/
RUN apt update
RUN apt install build-essential
RUN g++ ./src/main.cpp -o ./src/main
CMD ["uvicorn", "src.app:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
