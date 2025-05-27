from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, LongType, StringType
import sys

spark = SparkSession.builder \
    .appName("KafkaToSparkSelectFields") \
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0') \
    .getOrCreate()

payloadSchema = StructType([
    StructField("index", LongType(), True),
    StructField("gender", StringType(), True),
    StructField("race/ethnicity", StringType(), True),
    StructField("parental level of education", StringType(), True),
    StructField("lunch", StringType(), True),
    StructField("test preparation course", StringType(), True),
    StructField("math score", LongType(), True),
    StructField("reading score", LongType(), True),
    StructField("writing score", LongType(), True)
])

envelopeSchema = StructType([
    StructField("payload", StructType([
        StructField("before", payloadSchema, True),
        StructField("after", payloadSchema, True)
    ]), True)
])

df_raw = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka1:9092,kafka2:9092,kafka3:9092")
    .option("subscribe", "dbserver1.public.tmp")
    .option("startingOffsets", "earliest")
    .load()
)

df_after = (
    df_raw
    .selectExpr("CAST(value AS STRING) AS json_str")
    .select(from_json(col("json_str"), envelopeSchema).alias("env"))
    .select("env.payload.after.*")
)

df_selected = (
    df_after
    .select(
        col("gender"),
        col("race/ethnicity").alias("race_ethnicity"),
        col("parental level of education").alias("parental_education"),
        col("lunch"),
        col("test preparation course").alias("preparation_course"),
        col("math score").alias("math_score"),
        col("reading score").alias("reading_score"),
        col("writing score").alias("writing_score")
    )
)

# Define a function to write each micro-batch to MinIO (S3)
def write_to_minio(batch_df, batch_id):
    # Use Delta format; the S3 details are configured via Spark submit
    batch_df.write \
        .format("delta") \
        .mode("append") \
        .option("path", "s3a://spark-data/my-delta-table") \
        .save()

# Set up streaming query to write to MinIO
query = (
    df_selected.writeStream
    .foreachBatch(write_to_minio)
    .outputMode("append")
    .option("checkpointLocation", "s3a://spark-data/checkpoints/kafka_to_delta")
    .start()
)

console_query = (
    df_selected.writeStream
    .outputMode("append")
    .format("console")
    .option("truncate", False)
    .start()
)

# Await termination
query.awaitTermination(60_000)

if not query.isActive:
    spark.stop()
    sys.exit(0)
