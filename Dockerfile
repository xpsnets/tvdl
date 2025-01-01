FROM python:3.11-alpine

MAINTAINER xpsnets <xpsnets@outlook.com>
RUN mkdir /app
ADD ./main.py /app
ADD ./movieid.json /app
ADD ./requirements.txt /app
ADD ./config.py /app
WORKDIR /app  
RUN pip install -r requirements.txt
CMD ["python","-u","main.py"]