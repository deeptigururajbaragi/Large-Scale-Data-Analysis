# Project 1: Better Inverted Index Program 

* Author: Deepti Gururaj Baragi
* Class: CS535 Section 1
* Semester: 3 

## Overview
This Python program utilizes Hadoop's MapReduce framework to construct an inverted index from a collection of text documents. In addition to mapping word occurrences, it enhances the standard inverted index by ranking documents based on their relevance. The relevance is determined by the number of occurrences of the word within each document. This improvement ensures that the most relevant documents are positioned at the top of the search results. Even in cases where multiple documents have the same word count, they are sorted alphabetically to maintain consistency.  


## Reflection

During this project, I found the process of building an improved inverted index using Hadoop's MapReduce framework to be a valuable learning experience. What worked particularly well was the concept of ranking documents based on word occurrences, as it enhanced the understandability and readability of the output. The idea of employing a two-level sorting approach, initially by count and then alphabetically, added a layer of complexity to the project.

I encountered a memory issue during the initial stages of project that caused certain operations to be problematic. To address this, I allocated additional memory resources to the task and expanded the disk space. Additionally, I faced the issue of a "NameNode is in safe mode," which was caused by problems in the data nodes or potential file system corruption. To resolve this, I had to stop the DataNode and ResourceManager (YARN), and then reformat the Hadoop file system. Despite these challenges, I enjoyed working on this project as it provided an opportunity to apply and enhance my knowledge of MapReduce. 

## Compiling and Using

To compile and use this Inverted Index Python program, we should have a Linux environment and Hadoop installed on our system. This program can be run in either pseudo-distributed mode (on a single machine) or on a Hadoop cluster.

### Working on pseudo-distributed mode

Start Hadoop cluster in pseudo-distributed mode using the following commands:
   - Format the Hadoop filesystem (HDFS) namenode:
     `hdfs namenode -format`

   - Start the Hadoop daemons:
     `start-dfs.sh`

   - Check the status of the HDFS:
     `hdfs dfsadmin -report`

   - Create user directories for login name on the HDFS:
     `hdfs dfs -mkdir /user`

   - Start the YARN resource manager:
     `start-yarn.sh`

Clone the class-reources git repository using

`git clone https://github.com/BoiseState/CS535-resources`

Then on the terminal, configure hadoop to run on pseudo-distributed mode using,

`cd CS535-resources/examples/hadoop/local-scripts`
`./setmode.sh pseudo-distributed`

Then move to inverted-index directory which is in CS535-resources/examples/hadoop/inverted-index-python

As the small dataset test.txt is already present in 'inverted-index-python' directory, run

`cat test.txt | ./mapper.py | sort | ./reducer.py`

We can see the output which has list of words and the files in which the words are present. The files are reverse sorted by count.

### Working on cscluster

In cscluster, we need not install any tools or do any setup. We just need to login through ssh onyx to cscluster.

Here we need to setup a link from cluster to our local folder to work on large dataset

`cd ~
ln -s /home/amit/CS535-data/etext-data/etext-all etext-all`

Add the large dataset to input folder

`hdfs dfs -put etext-all`

Before running MapReduce program on hadoop cluster, make sure there are no outputs present in that path 

`hdfs dfs -ls`

Now run the hadoop command line to start MapReduce for the large dataset

time hadoop jar ~amit/hadoop-install/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar -mapper mapper.py -reducer reducer.py -input etext-all -output output -file ./mapper.py -file ./reducer.py

The above command contains time command as it is required to make observations on time taken to execute and run MapReduce job.

On finishing the MapReduce, check the output using

`hdfs dfs -get output`

Get to know the output folder name using ls command

Finally, select only small part of the dataset to make observation . This is recommened as the output will be very large for dataset with 594 files.

`head output/part-00000 -n 20`

In the above command line my output name is part-00000 which is in output folder. I am selecting first 20 outputs to be displayed. output/part-00000 -n 20


## Results 

I started this project in pseudo-distributed mode by running small dataset provided with the project.
The small test dataset test.txt consisted of
 
``` 
the the zebra zebra 
zebra 
and and 
00 
11
%$## 
44dbdb%% 
-ddd-$

```
On improving the MapReduce function as per the project requirement, the final output for the above test file was

```
and 2  test.txt 
ddd 1  test.txt 
the 2  test.txt 
zebra 3  test.txt 

```
After this, I moved on to work with large dataset that consisted 594 files. I ran this on csluster00 using hadoop command line, and the output was

```

aaa 6  rnpz810.txt, 1  jnglb10.txt, 1  pge0112.txt, 1  suall10.txt 
aaaa 1  rnpz810.txt 
aaaaaa 1  a1001108.txt 	
aaaaaah 1  pygml10.txt
aaaab 1  a1001108.txt
aaah 1  pygml10.txt 
aaarh 1  jnglb10.txt 	
aabborgt 1  pge0112.txt 
aachen 18  jm00v10.txt, 7  pge0112.txt, 2  8euhs10.txt, 2  bough11.txt, 2  hcath10.txt, 1  8dubc10.txt, 1  8fmtm10.txt, 1  8gtdr10.txt, 1  gn06v10.txt, 1  mtlad10.txt

```

The time command was also used while running MapReduce job for this large dataset and the time it took to run and execute this task was,

time

```
real	2m39.810s 
user	0m8.150s  
sys	0m0.551s

```
## Sources used

No other sources are used other than class files.

----------
This README template is using Markdown. Here is a quick cheat sheet on Markdown tags:
[https://www.markdownguide.org/cheat-sheet/](https://www.markdownguide.org/cheat-sheet/).
To preview your README.md output, you can view it on GitHub or in eclipse.
`

