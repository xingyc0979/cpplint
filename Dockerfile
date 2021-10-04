FROM ubuntu

WORKDIR /root

RUN echo "deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse" > /etc/apt/sources.list \
&& apt-get update \
&& apt-get install -y zip python python3-pip \
&& pip3 install cpplint

COPY ./run.py /root
COPY ./result_file.sh /root
CMD ["python3", "run.py"]
