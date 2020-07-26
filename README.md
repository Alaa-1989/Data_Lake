# Project: Data Lake
[Udacity](https://www.udacity.com/) Data Engineering Nanodegree Project

## Introduction
A music streaming startup, Sparkify, has grown their user base and song database even more and want to move their data warehouse to a data lake. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

### Our role is to:
- Building an ETL pipeline that extracts their data from S3, processes them using Spark, and loads the data back into S3 as a set of dimensional tables. 

This will allow their analytics team to continue finding insights in what songs their users are listening to.

## Project Description
In this project, we'll build an ETL pipeline for a data lake hosted on S3. 
- Load data from S3.
- Process the data into analytics tables using Spark.
- Load them back into S3. 
- Deploy this Spark process on a cluster using AWS.

## Datasets & ETL pipeline
We'll be working with two datasets that reside in S3. Here are the S3 links for each:
Song data: `s3://udacity-dend/song_data`
Log data: `s3://udacity-dend/log_data`

### Source Of Data
The [Million Song Dataset](http://millionsongdataset.com/) is a freely-available collection of audio features and metadata for a million contemporary popular music tracks. 

### Song Dataset
The first dataset is a subset of real data from the Million Song Dataset. Each file is in JSON format and contains metadata about a song and the artist of that song. 

### Log Dataset
The second dataset consists of log files in JSON format generated by this event simulator based on the songs in the dataset above.

## Database Schema
We use a star schema to create:

- Fact Table 
- Dimension Tables

![star schema](https://user-images.githubusercontent.com/42184553/83107280-a2971300-a0c6-11ea-8070-13f854605280.png)

### Fact Table
**songplays** - Records in log data associated with song plays.

### Dimension Tables
**users** - Users in the app.
**songs** - Songs in music database.
**artists** - Artists in music database.
**time** - Timestamps of records in songplays broken down into specific units.


## Project files

**etl.py** - Reads data from S3, processes that data using Spark, and writes them back to S3
**dl.cfgcontains** - AWS credentials
