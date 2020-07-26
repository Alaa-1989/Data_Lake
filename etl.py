import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
     """
    Launches a spark session
    """
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """
    Reads the songs JSON files from S3 and processes them with Spark.
    
    Args:
        input_data: Where to find the JSON input files.
        output_data: Where to save parquet files.
    """
    # get filepath to song data file
    song_data = input_data + 'song_data/*/*/*/*.json'
    
    # read song data file
    df = spark.read.json(song_data)

    # extract columns to create songs table
    songs_table = df.select('song_id', 'title', 'artist_id','year', 'duration').dropDuplicates()
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.partitionBy('year', 'artist_id').parquet(output_data + 'songs')

    # extract columns to create artists table
    artists_table = df.select('artist_id', 'artist_name', 'artist_location',
                              'artist_latitude', 'artist_longitude').dropDuplicates()
    
    # write artists table to parquet files
    artists_table.write.parquet(output_data + 'artists')


def process_log_data(spark, input_data, output_data):
    """
    Reads the logs JSON files from S3 and processes them with Spark.
    
    Args:
        input_data: Where to find the JSON input files.
        output_data: Where to save parquet files.
    """
    # get filepath to log data file
    log_data = input_data + 'log_data/*.json'

    # read log data file
    df = spark.read.json(log_data, schema = logdata_schema)
    
    # filter by actions for song plays
    df = df.filter(col("page") == 'NextSong')

    # extract columns for users table    
    artists_table = df.select(col("userId").alias("user_id"),
                              col("firstName").alias("first_name"),
                              col("lastName").alias("last_name"),
                              "gender","level")
    
    # write users table to parquet files
    artists_table.write.parquet(output_data+"users")

    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x: str(int(int(x)/1000)))
    df = df.withColumn('timestamp', get_timestamp(df.ts))
    
    # create datetime column from original timestamp column
    get_datetime = udf(lambda x: str(datetime.fromtimestamp(int(x) / 1000.0)))
    df = df.withColumn("datetime", get_datetime(df.ts))
    
    # extract columns to create time table
    time_table = time_table.select(col("ts").alias("start_time"),
                                   hour(col("ts")).alias("hour"),
                                   dayofmonth(col("ts")).alias("day"), 
                                   weekofyear(col("ts")).alias("week"), 
                                   month(col("ts")).alias("month"),
                                   year(col("ts")).alias("year"))
    
    # write time table to parquet files partitioned by year and month
    time_table.write.partitionBy("year","month").parquet(output_data+"time")

    # read in song data to use for songplays table
    song_df = spark.read.json(input_data + 'song_data/*/*/*/*.json')

    # extract columns from joined song and log datasets to create songplays table 
    songplays_table = song_df.join(df, song_df.artist_name==df.artist).withColumn("songplay_id", monotonically_increasing_id()).withColumn('start_time', to_timestamp(date_format((col("ts") /1000).cast(dataType=TimestampType()), tsFormat),tsFormat)).select("songplay_id","start_time",                         
           col("userId").alias("user_id"),
           "level",
           "song_id",
           "artist_id",
           col("sessionId").alias("session_id"),
           col("artist_location").alias("location"),
           "userAgent",
           month(col("start_time")).alias("month"),
           year(col("start_time")).alias("year"))

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.partitionBy("year","month").parquet(output_data+"songplays")


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = ""
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
