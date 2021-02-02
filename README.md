# dscc 402-202 Data Science at Scale

## Establishing a GitHub account
[Sign up for a new github account](https://docs.github.com/en/github/getting-started-with-github/signing-up-for-a-new-github-account) <br>
Fork the dsc402 repositiory into your new account.  Note: this will create a copy of the course repo for you to add and work on within your
own account.<br>
Goto https://github.com/lpalum/dsc402.git and hit the fork button while you are logged into your github account: ![fork image](https://github-images.s3.amazonaws.com/help/bootcamp/Bootcamp-Fork.png)

## Clone the dsc402 repository to get the class materials on your machine
<code>git clone https://github.com/[your account name]/dsc402.git</code><br>
note: you may want to clone this repo into a dirtory on your machine that you organize for code e.g. **/home/<your username>/code/github**

## Running your own local Spark Environment on your Computer
[Install docker on your computer](https://docs.docker.com/get-docker/)

Pull the all-spark-notebook image from docker hub: <br>
<code>https://hub.docker.com/r/lpalum/dsc402</code>
<br>Launch the docker image to open a Jupyter Lab instance in your local browser:<br>
<code>docker run -it --rm -p 8888:8888 --name all-spark --volume /home/[your account name]//code/github:/home/jovyan/work lpalum/dsc402 start.sh jupyter lab</code>

This will start a jupyter lab instance on your machine that you will be able to access at port 8888 in your browser and it will mount the github repo that you previouly
cloned into the containers working directory.

## Sign-up for the Community Edition of Databricks
[Databrick Community Edition FAQ](https://databricks.com/product/faq/community-edition)

import the DBC archive from the Learning Spark v2 github repositiory into your account.
[DBC Archive](https://github.com/databricks/LearningSparkV2/blob/master/notebooks/LearningSparkv2.dbc)

import the DBC archive for Project 1 from this repositiory into your account.
[Project 1 Archive](https://github.com/lpalum/dsc402/blob/master/notebooks/DSCC-202-402-Project1.dbc)
