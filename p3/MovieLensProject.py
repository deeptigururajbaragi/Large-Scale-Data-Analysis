#!/usr/bin/env python
# coding: utf-8

# In[1]:



# In[2]:


import warnings
warnings.filterwarnings('ignore')

import findspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType,  StringType, TimestampType, FloatType
import pyspark.sql.functions as fn
import os
import sys


# In[3]:


# # This below code was designed for Jupyter Notebook
# print('Please input path to folder location where movies.dat, users.dat, ratings.dat is available \n')
# folder_path = input()

# print('Please input path to folder where you want to store the output \n')
# output_folder_path = input()

# print('Please enter an integer to show top data\n')
# top_number = int(input())

# For Command Line Arguments

if len(sys.argv) != 4:
    print("Usage: MovieLensProject <inputFilesFolderPath> <outputFolderPath> <intNumberForTopValues>", file= sys.stderr)
    sys.exit(-1)
    
    
folder_path = sys.argv[1]
output_folder_path = sys.argv[2]
top_number = sys.argv[3]


# In[4]:


spark = SparkSession.builder.appName("MovieLens").getOrCreate()


# In[5]:


# Movies data reading
movie_cols = [ StructField("MovieID", IntegerType(), True),
               StructField("Title", StringType(), True),
               StructField("Genres", StringType(), True)
              ]
movie_schema = StructType(movie_cols)

df_movies = spark.read.csv(f'{folder_path}/movies.dat', sep = "::", header=False, schema = movie_schema)

# Split the Genres by |
df_movies = df_movies.withColumn("Genres", fn.explode(fn.split(df_movies["Genres"], "\\|")))


# In[6]:


# Users data reading

empty_rdd = spark.sparkContext.emptyRDD()

df_users = spark.createDataFrame(data = empty_rdd, schema = StructType([]))

if os.path.exists(f'{folder_path}/users.dat'):
    users_cols = [ StructField("UserID", IntegerType(), True),
                  StructField("Gender", StringType(), True),
                  StructField("Age", IntegerType(), True),
                  StructField("Occupation", IntegerType(), True),
                  StructField("Zip-code", IntegerType(), True)

    ]

    users_schema = StructType(users_cols)

    df_users = spark.read.csv(f'{folder_path}/users.dat', sep="::", header=False, schema=users_schema)

elif os.path.exists(f'{folder_path}/tags.dat'):
    tags_cols = [StructField("UserID", IntegerType(), True),
                StructField("MovieID", IntegerType(), True),
                StructField("Tags",StringType(),True),
                StructField("Timestamp", IntegerType(), True)
    ]
    tags_schema = StructType(tags_cols)
    df_users = spark.read.csv(f'{folder_path}/tags.dat', sep="::", header=False, schema=tags_schema)
    df_users = df_users.withColumn("TimestampParsed", fn.from_unixtime(fn.col("Timestamp")) )


# In[7]:


# Ratings data reading

ratings_cols = [StructField("UserID", IntegerType(), True),
                StructField("MovieID", IntegerType(), True),
                StructField("Rating",FloatType(),True),
                StructField("Timestamp", IntegerType(), True)

]

ratings_schema = StructType(ratings_cols)

df_ratings = spark.read.csv(f'{folder_path}/ratings.dat', sep = "::", header=False, schema = ratings_schema)

# Converting epoch seconds to timestamp

df_ratings = df_ratings.withColumn("TimestampParsed", fn.from_unixtime(fn.col("Timestamp")) )


# ### Creating temp tables/views for the dataframes

# In[8]:


df_movies.createOrReplaceTempView("Movies")
df_ratings.createOrReplaceTempView("Ratings")

if df_users.count() > 0:
    df_users.createOrReplaceTempView("Users")


# ## 1. Top 5 Genres in each year

# In[9]:


sql_query = '''
            SELECT CAST(ratingYear AS STRING) AS ratingYearStr, Genres, CAST(avgRating AS STRING) avgRatingstr 
            FROM (
                    SELECT Genres, ratingYear, avgRating, DENSE_RANK() OVER (PARTITION BY ratingYear ORDER BY avgRating DESC) rnk
                    FROM (
                            SELECT Genres, ratingYear, ROUND(AVG(Rating), 2) avgRating
                            FROM (
                                    SELECT m.Title, m.Genres, r.Rating, EXTRACT(YEAR FROM r.TimestampParsed) as ratingYear
                                    FROM Movies m
                                    INNER JOIN Ratings r
                                        ON r.MovieID = m.MovieID
                                ) t
                            GROUP BY Genres, ratingYear
                        ) b
                ) c
            WHERE rnk <= 5
            '''

# Save the result of the query to a text file
df_top_genres = spark.sql(sql_query)
df_top_genres = df_top_genres.withColumn("op", fn.concat_ws(",", fn.col("ratingYearStr"), fn.col("Genres"), fn.col("avgRatingstr")))

df_top_genres.select("op").write.text(f'{output_folder_path}/top_genres_each_year')


# ## 2. What are the k most popular movies for each season (summer, fall, winter, spring)?

# In[10]:


sql_query = '''
            SELECT season, Title, CAST(avgRating AS STRING) avgRatingstr
            FROM (
                    SELECT season, Title, avgRating, 
                           DENSE_RANK() OVER (PARTITION BY season ORDER BY avgRating DESC) rnk
                    FROM (
                            SELECT r.season, m.Title, AVG(Rating) avgRating
                            FROM (
                                    SELECT MovieId, Rating,
                                        CASE
                                            WHEN month(cast(TimestampParsed AS date)) IN (12, 1, 2) THEN 'Winter'
                                            WHEN month(cast(TimestampParsed AS date)) IN (3, 4, 5) THEN 'Spring'
                                            WHEN month(cast(TimestampParsed AS date)) IN (6, 7, 8) THEN 'Summer'
                                            WHEN month(cast(TimestampParsed AS date)) IN (9, 10, 11) THEN 'Fall'
                                            ELSE 'Invalid Month'
                                        END AS season
                                    FROM Ratings
                                ) r
                            INNER JOIN Movies m
                                ON m.MovieId = r.MovieId
                            GROUP BY r.season, m.Title
                    ) b
                ) c
            WHERE rnk <= {}
            '''.format(top_number)


# Save the result of the query to a text file
df_season_top = spark.sql(sql_query)
df_season_top = df_season_top.withColumn("op", fn.concat_ws(",", fn.col("season"), fn.col("Title"), fn.col('avgRatingstr')))

df_season_top.select("op").write.text(f'{output_folder_path}/top_season')


# ##  3. What are the k most popular movies of all time?
# 

# In[11]:


sql_query = '''SELECT DISTINCT m.Title, CAST(avgRating AS STRING) avgRatingstr
               FROM Movies m
               INNER JOIN (
                           SELECT MovieID, ROUND(AVG(Rating),2) AS avgRating
                           FROM Ratings
                           GROUP BY MovieID
                    ) r
                       ON m.MovieID = r.MovieID
              ORDER BY avgRatingstr DESC
              LIMIT {}

            '''.format(top_number)
# Save the result of the query to a text file
df_top_rated = spark.sql(sql_query)
df_top_rated = df_top_rated.withColumn("op", fn.concat_ws(",", fn.col("Title"), fn.col('avgRatingstr')))
df_top_rated.select("op").write.text(f'{output_folder_path}/top_rated')


# 

# ## 4. What are the k most popular movies for a particular year?

# In[12]:


sql_query = '''SELECT DISTINCT m.Title, CAST(r.avgRating AS STRING) avgRatingstr
               FROM Movies m
               INNER JOIN (
                           SELECT MovieID, ROUND(AVG(Rating),2) AS avgRating
                           FROM Ratings
                           WHERE EXTRACT(YEAR FROM TimestampParsed) = {}
                           GROUP BY MovieID
                    ) r
                       ON m.MovieID = r.MovieID
              ORDER BY avgRatingstr DESC
              LIMIT {}

            '''.format(2000, top_number)

df_top_rated_year = spark.sql(sql_query)
df_top_rated_year = df_top_rated_year.withColumn("op", fn.concat_ws(",", fn.col("Title"), fn.col('avgRatingstr')))
df_top_rated_year.select("op").write.text(f'{output_folder_path}/top_rated_year_2000')


# ## 5. What are the k most popular movies based on gender?
# 
# This part will only execute if the `users.dat` have __Gender__ column available i.e. for 1M dataset

# In[13]:


if 'Gender' in df_users.columns:
    
    sql_query = '''
                    SELECT DISTINCT u.Gender, m.Title, ROUND(AVG(ra.Rating),2) AS avgRating, COUNT(ra.Rating) AS ratingCount
                    FROM Movies m
                    INNER JOIN Ratings ra ON m.MovieID = ra.MovieID
                    INNER JOIN Users u ON ra.UserID = u.UserID
                    WHERE u.Gender = 'F'
                    GROUP BY m.Title, u.Gender
                    HAVING ratingCount >= 250 --filtering out movies with less ratings to avoid skewness in result
                    ORDER BY avgRating DESC
                    LIMIT {}
                '''.format(top_number)

    
    
    df_top_rated_gender = spark.sql(sql_query)
    df_top_rated_gender = df_top_rated_gender.withColumn("avgRatingstr", fn.col("avgRating").cast("string"))
    df_top_rated_gender = df_top_rated_gender.withColumn("op", fn.concat_ws(",", fn.col("Gender"), fn.col("Title"), fn.col('avgRatingstr')))
    df_top_rated_gender.select("op").write.text(f'{output_folder_path}/top_rated_gender')


# ## 6. What are the top k movies with the most ratings (presumably most popular) that have the lowest ratings?

# In[14]:


sql_query = ''' SELECT DISTINCT  m.Title, CAST(averageRatings AS STRING) averageRatings, CAST(totalRatings AS STRING) totalRatings
                FROM Movies m
                INNER JOIN(
                            SELECT MovieID, COUNT(Rating) AS totalRatings, ROUND(AVG(Rating),2) AS averageRatings
                            FROM Ratings
                            GROUP BY MovieID

                )r
                    ON m.MovieID = r.MovieID
                ORDER BY averageRatings ASC, totalRatings DESC
                LIMIT {}

            '''.format(top_number)
df_high_count_low_rated = spark.sql(sql_query)
df_high_count_low_rated = df_high_count_low_rated.withColumn("averageRatingsstr", fn.col("averageRatings").cast("string"))
df_high_count_low_rated = df_high_count_low_rated.withColumn("totalRatingsstr", fn.col("totalRatings").cast("string"))
df_high_count_low_rated = df_high_count_low_rated.withColumn("op", fn.concat_ws(",", fn.col("Title"), fn.col('averageRatingsstr'), fn.col('totalRatingsstr')))
df_high_count_low_rated.select("op").write.text(f'{output_folder_path}/high_count_low_rated')

