FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
ADD install_solc.sh /app/
RUN pip install py-solc && python -m solc.install v0.4.24
RUN pip install --no-cache-dir  -r requirements.txt