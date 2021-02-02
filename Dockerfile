FROM jupyter/all-spark-notebook

USER root
RUN apt-get update && apt-get install -y gnupg

RUN echo "deb https://dl.bintray.com/sbt/debian /" | tee -a /etc/apt/sources.list.d/sbt.list
RUN curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | apt-key add
RUN apt-get update
RUN apt-get install sbt

RUN python -m pip install --upgrade pip
RUN python -m pip install \
    pyspark==3.0.1 \
    mlflow==1.12.1 \
    boto3==1.16.25 

# -- Runtime
EXPOSE 8888
EXPOSE 4040-4049



