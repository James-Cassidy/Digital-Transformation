FROM ubuntu:20.04
RUN apt-get update -y && apt-get install -y python3-pip python3
WORKDIR /app
RUN pip3 install Flask 
RUN pip3 install jwt
RUN pip3 install requests
RUN pip3 install Flask-Cors
COPY ./src /app
EXPOSE 3307
ENTRYPOINT [ "python3" ]
CMD ["login_reg_and_auth.py"]
