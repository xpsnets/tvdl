FROM python:3.6-alpine

MAINTAINER xpsnets <xpsnets@outlook.com>

ADD ./synopy /app/synopy
ADD ./main.py /app
ADD ./movieid.json /app
ADD ./requirements.txt /app
WORKDIR /app  
RUN pip install -r requirements.txt
CMD ["python","-u","main.py"]