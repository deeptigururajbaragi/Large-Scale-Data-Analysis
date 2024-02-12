# Project 3: Data Science with Spark

## Overview

In this project, we utilize PySpark to explore the MovieLens dataset, emphasizing the discernment
of patterns and trends. Leveraging PySpark's capabilities, our analysis covers popular genres,
seasonal hits, yearly standouts, and the evolution of favorite movies over time. Delving deeper,
we examine how audience preferences vary based on gender and investigate rating discrepancies,
revealing instances where highly rated movies coexist with lower ratings.


## Compiling and Using

The program can be compiled and run in Google Colab, prompting users to provide input paths and
customize parameters, including the number of rows to be displayed and preferences for trends
such as top movies based on the year or gender. Additionally, the program is compatible with a
Linux environment where Spark is installed. We successfully executed the program in both Google
Colab and cscluster environments.

Our Python file requires the following command line arguments
```
MovieLensProject.py <inputFilesFolderPath> <outputFolderPath> <intNumberForTopValues>
```

To run on the Spark cluster use the following command
```
spark-submit --master local[4] MovieLensProject.py <inputFilesFolderPath> <outputFolderPath> <intNumberForTopValues>
```

## Results 
1. `output-1million` this folder contains the output for 1 million dataset which we executed
on cluster. Since the size of the input wa too large so we did not add the input.

2.  `outputsplit` to enable input loading to git repo we split 1 million dataset so that the
size becomes less than 10 MB. The reduced size input is available in `ml-1m-split` and the folder
`outputsplit` is the output for same .


## Sources used

We haven't used any sources outside of the class materials.

----------
This README template is using Markdown. Here is a quick cheat sheet on Markdown tags:
[https://www.markdownguide.org/cheat-sheet/](https://www.markdownguide.org/cheat-sheet/).
To preview your README.md output, you can view it on GitHub or in eclipse.

