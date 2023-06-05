FROM ubuntu:20.04
RUN apt-get update -y && apt-get install -y python3-pip python3
WORKDIR /app
RUN pip3 install Flask 
RUN pip3 install requests
RUN pip3 install PyMySQL
RUN pip3 install passlib
COPY ./src /app
EXPOSE 3306
ENTRYPOINT [ "python3" ]
CMD ["awsdbapp.py"]
