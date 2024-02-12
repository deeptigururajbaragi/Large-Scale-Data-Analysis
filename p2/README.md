# Project 2: Better Inverted Index Using Spark

* Author: Deepti Gururaj Baragi

## Overview

This Python program employs Spark to create a better inverted index for a collection of text documents. It enhances the standard inverted index by ranking documents according to their relevance, determined by word occurences within each document. The program ensures that the most relevant documents are placed at the top of the search results, maintaining alphabetical sorting incase of equal word counts. 


## Compiling and Using

To compile and run this Better Inverted Index Python program, we can use Google Colab and specify the input and output paths accordingly. We can also use Linux environment in which Spark is installed. This program can be run in either pseudo-distributed mode (on a single machine) or on a Hadoop cluster.

### Working on pseudo-distributed mode

Start Spark in pseudo-distributed mode using 'pyspark' in the command line:

``` 
pyspark

```
Clone the class-resources git repository using

```
git clone https://github.com/BoiseState/CS535-resources

```

Then move to the 'wordcount' directory

```
cd CS535-resources/examples/spark/wordcount

```

I have added new python script 'better_inverted_index.py' to the wordcount directory, as the small input on which we need to run our script is already present there.

To run the 'better_inverted_index.py' locally we can use the command line:

```
time spark-submit –master local[4] better_inverted_index.py
```
The above command contains time command as it is required to make observations on time taken to execute and run the job.
I have already included the input paths in my python script. If we want to use any other input, we can update the input path.
Also to run the large dataset locally, I copied the large dataset 'etext-all' to the same wordcount directory to make it easier for execution.

The output for this will be saved in an output folder in the same directory 'wordcount' as I have already specified the output path in my python script. The output will be distributed into several parts. 

We can run Spark locally on our machine without using HDFS.

### Working on cluster

In cscluster, we need not install any tools or do any setup. We just need to login through ssh onyx to cscluster.

Here we need to setup a link from cluster to our local folder to work on large dataset

```

cd ~ ln -s /home/amit/CS535-data/etext-data/etext-all etext-all

```

Add the large dataset to input folder
```
hdfs dfs -put etext-all 
```

Before running the script in cluster, make sure there are no outputs present in that path

```
hdfs dfs -ls
```

Now run the Spark command line for large dataset

```
time spark-submit --master spark://cscluster00.boisestate.edu:7077 better_inverted_index.py hdfs://cscluster00.boisestate.edu:9000/user/deeptigururajbar/etext-all hdfs://cscluster00.boisestate.edu:9000/user/deeptigururajbar/output

```

On running this, the output will be saved in hdfs and can be checked using

```
hdfs dfs -ls
```


## Results 

I started this project in pseudo-distributed mode by running small dataset provided with the project. The small dataset consisted of 14 text files. On creating a better inverted index program as per the project requirement, the final output for the input with 14 text files was

```
to 28973  Encyclopaedia.txt, 19819  Complete-Shakespeare.txt, 13924  Les-Miserables.txt, 2029  Scarlet-Letter.txt, 1061  Flatland.txt, 854  Tom-Sawyer-Abroad.txt, 781  Through-the-Looking-Glass.txt, 778  Alice-in-Wonderland.txt, 147  US-Constitution.txt, 98  Decl-of-Ind-USA.txt, 89  Gift-of-the-Magi.txt, 83  Patrick-Henry.txt, 56  Bill-of-Rights.txt, 8  Gettysburg-Address.txt
world 905  Complete-Shakespeare.txt, 315  Encyclopaedia.txt, 202  Les-Miserables.txt, 90  Scarlet-Letter.txt, 27  Tom-Sawyer-Abroad.txt, 21  Flatland.txt, 7  Alice-in-Wonderland.txt, 5  Decl-of-Ind-USA.txt, 5  Through-the-Looking-Glass.txt, 3  Patrick-Henry.txt, 2  Bill-of-Rights.txt, 2  US-Constitution.txt, 1  Gettysburg-Address.txt
of 73269  Encyclopaedia.txt, 19878  Les-Miserables.txt, 18191  Complete-Shakespeare.txt, 3314  Scarlet-Letter.txt, 1525  Flatland.txt, 586  Tom-Sawyer-Abroad.txt, 551  Alice-in-Wonderland.txt, 527  Through-the-Looking-Glass.txt, 324  US-Constitution.txt, 119  Decl-of-Ind-USA.txt, 85  Gift-of-the-Magi.txt, 82  Patrick-Henry.txt, 64  Bill-of-Rights.txt, 5  Gettysburg-Address.txt
zip   2 Alice-in-Wonderland.txt, 2 Complete-Shakespeare.txt, 2 Encyclopaedia.txt, 2 Flatland.txt, 2 Gift-of-the-Magi.txt, 2 Les-Miserables.txt, 2 Scarlet-Letter.txt, 2 Through-the-Looking-Glass.txt, 2 Tom-Sawyer-Abroad.txt, 1 Bill-of-Rights.txt, 1 Decl-of-Ind-USA.txt, 1 Patrick-Henry.txt, 1 US-Constitution.txt
being   1753 Encyclopaedia.txt, 664 Complete-Shakespeare.txt, 469 Les-Miserables.txt, 66 Scarlet-Letter.txt, 57 Flatland.txt, 23 Through-the-Looking-Glass.txt, 20 Alice-in-Wonderland.txt, 11 Tom-Sawyer-Abroad.txt, 5 Gift-of-the-Magi.txt, 1 Bill-of-Rights.txt, 1 US-Constitution.txt


```

After this, I ran large dataset that consisted of 594 files in pseudo-distributed mode and the output was,

```

grieuances 4  00ws110.txt
whitenesse 4  00ws110.txt
boughes 7  cbtls12.txt, 6  00ws110.txt, 2  lcjnl10.txt, 1  bough11.txt
hostilitie 3  00ws110.txt
exigent 3  00ws110.txt, 3  roget15a.txt, 2  suall10.txt, 1  2ws0110.txt, 1  2ws2410.txt, 1  2ws3510.txt, 1  g1001108.txt, 1  ggpnt10.txt, 1  shndy10.txt, 1  tmbn210.txt

```

Then I ran the same large dataset consisting of 594 files in cluster and the output was,

```

dishonoureth   3 kjv10.txt, 2 2drvb10.txt, 2 f1001108.txt, 1 51001108.txt, 1 a1001108.txt, 1 b1001108.txt, 1 e1001108.txt, 1 tftaa10.txt
grandfathers   4 drthn11.txt, 4 eduha10.txt, 3 2cahe10.txt, 3 71001108.txt, 3 agino10.txt, 3 bygdv10.txt, 3 gn06v10.txt, 2 1cahe10.txt, 2 8gtdr10.txt, 2 8hsrs10.txt, 2 dscmn10.txt, 2 gm00v11.txt, 2 humbn10.txt, 2 irish10.txt, 2 mohic10.txt, 2 tmrcr10.txt, 1 1drvb10.txt, 1 1mrar10.txt, 1 1vkip11.txt, 1 31001108.txt, 1 3linc11.txt, 1 8aggr10.txt, 1 8homr10.txt, 1 8rtib10.txt, 1 8tomj10.txt, 1 8ushx10.txt, 1 avon10.txt, 1 b033w10.txt, 1 bough11.txt, 1 btowe10.txt, 1 cpogs10.txt, 1 cs10w10.txt, 1 g1001108.txt, 1 idiot10.txt, 1 ironm11.txt, 1 jungl10.txt, 1 legva12.txt, 1 lesms10.txt, 1 lflcn10.txt, 1 lgtrd10.txt, 1 mdmar10.txt, 1 mdvll10.txt, 1 mn20v11.txt, 1 mtlad10.txt, 1 phrlc10.txt, 1 repub13.txt, 1 tess10.txt, 1 totlc10.txt, 1 vfair12.txt, 1 wrnpc10.txt
aspirations   34 suall10.txt, 15 irish10.txt, 15 jm00v10.txt, 14 inagu10.txt, 14 uspis10.txt, 13 gn06v10.txt, 10 8romn10.txt, 10 btowe10.txt, 9 b033w10.txt, 9 pge0112.txt, 8 1vkip11.txt, 7 8unlt10.txt, 6 8luth10.txt, 6 idiot10.txt, 6 shlyc10.txt, 5 2musk10.txt, 5 8rheb10.txt, 5 lflcn10.txt, 5 mrclt10.txt, 4 8swan11.txt, 4 janey11.txt, 4 lesms10.txt, 4 lfcpn10.txt, 3 8purg10.txt, 3 8shkm10.txt, 3 andvl11.txt, 3 bough11.txt, 3 fkchp10.txt, 3 fs40w10.txt, 3 mtlad10.txt, 3 samur10.txt, 3 sffrg10.txt, 3 soulb10.txt, 3 strtt10.txt, 3 tgovt10.txt, 3 twrdn10.txt, 2 0ddcl10.txt, 2 1donq10.txt, 2 1onwr10.txt, 2 2city12.txt, 2 8csus10.txt, 2 8elit10.txt, 2 8euhs10.txt, 2 8gtdr10.txt, 2 8idol10.txt, 2 8swnn10.txt, 2 avon10.txt, 2 cnstr10.txt, 2 cprfd10.txt, 2 cprrn10.txt, 2 drthn11.txt, 2 dscep10.txt, 2 gm00v11.txt, 2 hcath10.txt, 2 hdark12a.txt, 2 hoend10.txt, 2 jude11.txt, 2 pmisr10.txt, 2 prblm10.txt, 2 scrlt12.txt, 2 thjwl10.txt, 2 wlwrk10.txt, 2 wrnpc10.txt, 1 1cahe10.txt, 1 1linc11.txt, 1 2linc11.txt, 1 7linc11.txt, 1 8crmp10.txt, 1 8igjp10.txt, 1 8jrc710.txt, 1 8moor10.txt, 1 8ntle10.txt, 1 8rbaa10.txt, 1 8sced10.txt, 1 8vnmm10.txt, 1 8wwrt10.txt, 1 a1001108.txt, 1 agnsg10.txt, 1 andsj10.txt, 1 bgita10.txt, 1 bnrwy10.txt, 1 canpw10.txt, 1 carol13.txt, 1 curio10.txt, 1 cwgen11.txt, 1 dchla10.txt, 1 dnhst10.txt, 1 duglas11.txt, 1 frank14.txt, 1 g138v10.txt, 1 gmars12.txt, 1 grexp10a.txt, 1 hardt10.txt, 1 hbtht10.txt, 1 hphnc10.txt, 1 ironm11.txt, 1 jandc10.txt, 1 koran12a.txt, 1 lacob11.txt, 1 lwmen12.txt, 1 mbova10.txt, 1 mdntp10.txt, 1 mdvll10.txt, 1 milnd11.txt, 1 moby11.txt, 1 nativ10.txt, 1 nb17v11.txt, 1 phado10.txt, 1 phrlc10.txt, 1 plpwr10.txt, 1 poe2v10.txt, 1 poe3v11.txt, 1 prtrt10.txt, 1 repub13.txt, 1 resur10.txt, 1 rob3w10.txt, 1 rosry11.txt, 1 rplan10.txt, 1 scarr10.txt, 1 shkdd10.txt, 1 spzar10.txt, 1 tarzn10.txt, 1 tbisp10.txt, 1 tess10.txt, 1 tfdbt10.txt, 1 timem11.txt, 1 totlc10.txt, 1 trabi10.txt, 1 truss10.txt, 1 ulyss12.txt, 1 vfear11a.txt, 1 vstil10.txt, 1 wflsh10.txt, 1 wuthr10.txt
rods   67 fb10w11.txt, 21 plivs10.txt, 15 kjv10.txt, 14 wlwrk10.txt, 13 mohic10.txt, 12 1drvb10.txt, 12 bough11.txt, 12 moby11.txt, 10 jm00v10.txt, 9 pge0112.txt, 8 gn06v10.txt, 7 2lotj10.txt, 7 andvl11.txt, 6 2drvb10.txt, 6 8ldvc10.txt, 6 g1001108.txt, 6 gm00v11.txt, 6 sp85g10.txt, 5 11001108.txt, 5 41001108.txt, 5 h8ahc10.txt, 5 mdvll10.txt, 4 00ws110.txt, 4 1vkip11.txt, 4 dchla10.txt, 4 mbova10.txt, 4 mn20v11.txt, 4 mtrcs10.txt, 4 pas8w10.txt, 3 1hofh10.txt, 3 2rbnh10.txt, 3 2yb4m10.txt, 3 3lotj10.txt, 3 8euhs10.txt, 3 shlyc10.txt, 3 warje10.txt, 2 1lotj10.txt, 2 3drvb10.txt, 2 61001108.txt, 2 80day11.txt, 2 8aggr10.txt, 2 8igjp10.txt, 2 8moon10.txt, 2 8year10.txt, 2 anide10.txt, 2 benhr10.txt, 2 bhawk10.txt, 2 btowe10.txt, 2 c1001108.txt, 2 duglas11.txt, 2 f1001108.txt, 2 g138v10.txt, 2 ggpnt10.txt, 2 iliad10b.txt, 2 jungl10.txt, 2 kalec10.txt, 2 koran12a.txt, 2 lcjnl10.txt, 2 llake10.txt, 2 milnd11.txt, 2 poe1v10.txt, 2 ssklt10.txt, 2 tfdbt10.txt, 2 tftaa10.txt, 2 vfair12.txt, 2 vstil10.txt, 2 warw12.txt, 2 wnbrg11.txt, 1 1mart10.txt, 1 2city12.txt, 1 2dfre11.txt, 1 2hofh10.txt, 1 2ws1410.txt, 1 2ws1910.txt, 1 2ws2110.txt, 1 2ws3510.txt, 1 4lotj10.txt, 1 51001108.txt, 1 71001108.txt, 1 81001108.txt, 1 8clln10.txt, 1 8eftl10.txt, 1 8hmvg10.txt, 1 8jrc710.txt, 1 8ntle10.txt, 1 8rome10.txt, 1 8rtib10.txt, 1 8tspv111.txt, 1 8tspv211.txt, 1 8ushx10.txt, 1 aaard10.txt, 1 arjpl10.txt, 1 b033w10.txt, 1 bllfn10.txt, 1 bnrwy10.txt, 1 cbtls12.txt, 1 chldh10.txt, 1 chshr10.txt, 1 clckm10.txt, 1 cpogs10.txt, 1 cprfd10.txt, 1 cptcr11a.txt, 1 cwgen11.txt, 1 gltrv10.txt, 1 grimm10.txt, 1 hmjnc10.txt, 1 hmjnc11.txt, 1 holyw10.txt, 1 hphnc10.txt, 1 lesms10.txt, 1 lflcn10.txt, 1 lgtrd10.txt, 1 mohwk10.txt, 1 mwktm10a.txt, 1 orfur10.txt, 1 pcwar10.txt, 1 poe3v11.txt, 1 poe4v10.txt, 1 prtrt10.txt, 1 resur10.txt, 1 rgain10.txt, 1 rob3w10.txt, 1 sign410.txt, 1 slman10.txt, 1 sprvr11.txt, 1 spzar10.txt, 1 st15w10.txt, 1 suall10.txt, 1 tarzn10.txt, 1 tbyty10.txt, 1 tcosa10.txt, 1 tess10.txt, 1 thjwl10.txt, 1 trabi10.txt, 1 wrnpc10.txt
scorched 15  gn06v10.txt, 7  8tjna10.txt, 6  dnhst10.txt, 6  janey11.txt, 6  moby11.txt, 6  shlyc10.txt, 6  warw12.txt, 5  bough11.txt, 4  lesms10.txt, 4  lwmen12.txt, 3  3drvb10.txt, 3  5dfre11.txt, 3  blkhs10.txt, 3  ftroy10.txt, 3  gm00v11.txt, 3  kjv10.txt, 3  nkrnn11.txt, 3  pgbev10.txt, 3  wrnpc10.txt, 3  wtfng10.txt, 2  0ddcl10.txt, 2  21001108.txt, 2  5wiab10.txt, 2  71001108.txt, 2  8grtr10.txt, 2  8jrc710.txt, 2  cs10w10.txt, 2  cstwy11.txt, 2  ironm11.txt, 2  lcjnl10.txt, 2  nc13v11.txt, 2  pcwar10.txt, 2  pge0112.txt, 2  scarp10.txt, 2  spzar10.txt, 2  timem11.txt, 2  zambs10.txt, 1  00ws110.txt, 1  1argn10.txt, 1  1hofh10.txt, 1  1mrar10.txt, 1  1vkip11.txt, 1  2cahe10.txt, 1  2city12.txt, 1  2dfre11.txt, 1  2hofh10.txt, 1  2musk10.txt, 1  2ws1410.txt, 1  3lotj10.txt, 1  4lotj10.txt, 1  80day11.txt, 1  8augr10.txt, 1  8elit10.txt, 1  8hfld10.txt, 1  8josh10.txt, 1  8ldvc10.txt, 1  8moor10.txt, 1  8purg10.txt, 1  8romn10.txt, 1  8rran10.txt, 1  armyl10.txt, 1  avon10.txt, 1  badge10a.txt, 1  baron10.txt, 1  benhr10.txt, 1  bllfn10.txt, 1  bwulf11.txt, 1  callw10.txt, 1  cbtls12.txt, 1  cfvrw10.txt, 1  comet10.txt, 1  cprfd10.txt, 1  dchla10.txt, 1  dmsnd11.txt, 1  doroz10.txt, 1  ebacn10.txt, 1  g138v10.txt, 1  ggpnt10.txt, 1  gp37w10.txt, 1  grexp10a.txt, 1  hfinn12.txt, 1  hmjnc10.txt, 1  hmjnc11.txt, 1  hoend10.txt, 1  homer10.txt, 1  icfsh10.txt, 1  ithoa10.txt, 1  jm00v10.txt, 1  jungl10.txt, 1  lgsp10.txt, 1  memho11.txt, 1  mhyde10.txt, 1  mn20v11.txt, 1  mohic10.txt, 1  moon10.txt, 1  mormon13.txt, 1  nb17v11.txt, 1  olivr10.txt, 1  ozland10.txt, 1  phant12.txt, 1  plivs10.txt, 1  plrabn12.txt, 1  rosry11.txt, 1  rshft10.txt, 1  sawyr11.txt, 1  scrlt12.txt, 1  shrhe10.txt, 1  siddh10.txt, 1  suall10.txt, 1  tagod10.txt, 1  thdcm10.txt, 1  tmrcr10.txt, 1  truss10.txt, 1  vbgle11a.txt, 1  wltnt10.txt, 1  wwend10.txt

```
Here, only 5 outputs are there as I have specified in my Python script to get the first 5 results using take(5).
The time command was also used to run large dataset in both pseudo-distributed mode as well as in cluster.

In pseudo-distributed mode, the time it took to run and execute the task was,

```

real	7m20.995s
user	0m33.478s
sys	0m18.150s

```

In cluster, the time it took to run and execute the task was,

```

real	2m30.622s
user	0m16.007s
sys	0m1.040s

```
### Comparison of runtime

#### Spark Pseudo-distributed vs Spark Cluster mode:

| Spark Pseudo-distributed      | Spark Cluster     | 
| ------------------------------|--------------------
| real    7m20.995s             | real    2m30.622s |
| user    0m33.478s             | user    0m16.007s |   
| sys     0m18.150s             | sys     0m1.040s  |    

The runtime in cluster mode is significantly faster than in pseudo-distributed mode. This is expected as the cluster mode utilizes multiple nodes for parallel processing.

#### Spark cluster vs Hadoop cluster:

| Spark cluster                 | Hadoop Cluster     |    
| ------------------------------|--------------------
| real     2m30.622s            | real    2m39.810s  |
| user     0m16.007s            | user    0m8.150s   | 
| sys      0m1.040s             | sys     0m0.551s   |   

The Spark cluster outperforms the Hadoop cluster. Spark's in-memory processing and optimization techniques often lead to faster data processing compared to traditional Hadoop MapReduce.

#### Spark Pseduo-distributed vs Hadoop Pseudo-distributed:

| Spark Pseudo-distributed      | Hadoop Pseudo-distributed | 
| ------------------------------|--------------------------
| real  7m20.995s               | real   29m5.600s          |
| user  0m33.478s               | user   0m34.567s          |
| sys   0m18.150s               | sys    0m5.162s           |

The Spark pseduo-distributed is faster than Hadoop pseudo-distributed due to its emphasis on in-memory processing, reducing disk I/O bottlenecks and enhancing overall execution efficiency.



## Sources used

No other sources are used other than class files.

----------
This README template is using Markdown. Here is a quick cheat sheet on Markdown tags:
[https://www.markdownguide.org/cheat-sheet/](https://www.markdownguide.org/cheat-sheet/).
To preview your README.md output, you can view it on GitHub or in eclipse.
