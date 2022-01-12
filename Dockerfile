FROM public.ecr.aws/lts/ubuntu:latest
MAINTAINER tsukiyashirokisaki
RUN apt update -y
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa 
RUN apt update -y
RUN apt install python3.8 -y
RUN ln -s /usr/bin/python3.8 /usr/bin/python
RUN apt-get update -y
RUN apt-get install git -y
RUN apt-get install python3-pip -y
RUN pip3 install flask
RUN pip3 install python-dotenv
RUN echo "566"
RUN git clone https://github.com/tsukiyashirokisaki/nfv_final
CMD cd nfv_final && flask run --host=0.0.0.0
