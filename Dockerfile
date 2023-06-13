FROM python:3.10.6-buster

WORKDIR /prod

#install dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#install taxifare
COPY CLASSML CLASSML
COPY api api
COPY setup.py setup.py
RUN pip install .

#reset local_files
COPY Makefile Makefile
RUN make reset_local_files

CMD uvicorn taxifare.api.fast:app --host 0.0.0.0 --port $PORT
