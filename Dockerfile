FROM python:3

WORKDIR /usr/src/app/crawler

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt
RUN playwright install
RUN playwright install-deps

COPY . .

CMD [ "python3", "./run-spiders.py" ]