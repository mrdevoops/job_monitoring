FROM python:3
COPY ./app /app
WORKDIR /app 
RUN pip install -r /app/requirements.txt
CMD ["/usr/local/bin/python", "web.py"]
EXPOSE 8000


