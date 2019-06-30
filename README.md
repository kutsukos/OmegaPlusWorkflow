
# OmegaPlus Kutsukos Workflow 2
This series of steps was used to detect positive selection on ERV insertions in the human genome. For this example, we are going to use only two ERV insertions.

**Don't forget!** During this example-workflow, we are talking about ERVs insertions in human genome. This example may apply to insertions in other species. Use it wisely!



# Table of contents
1. [Required applications and OS](#reqs)
2. [Step 1 - Project initialization and OmegaPlus downloading](#step1)
2. [Step 2 - Preparation of the required data ](#step2)
   1. [Step 2.1 - ERV Insertions Information](#step21)
   2. [Step 2.2 - Samples extraction from vcf file](#step22)
   3. [Step 2.3 - Grid points selection](#step23)
   4. [Step 2.4 - Files downloading for analysis](#step24)
3. [Step 3 - Preparing OmegaPlus commands](#step3)
4. [Step 4 - Executing OmegaPlus commands](#step4)
5. [Step 5 - Control runs](#step5)
6. [Step 6 - Preparation of the required data for control runs](#step6)
   1. [Step 6.1 - Files downloading for analysis](#step61)
   2. [Step 6.2 - Grid points selection REMINDER!](#step62)
7. [Step 7 - Preparing OmegaPlus control commands](#step7)
8. [Step 8 - Executing OmegaPlus control commands](#step8)
9. [Step 9 - Visualization of OmegaPlus results ](#step9)
12. [Citations](#cite)
13. [Version Changelog](#version)
14. [Contact](#contact)

## Required applications and OS <a name="reqs"></a>
[![uses-bash](https://img.shields.io/badge/Uses%20-Bash-blue.svg)](https://www.gnu.org/software/bash/)
[![Python 2.7](https://img.shields.io/badge/Python-2.7-green.svg)](https://www.python.org/)
[![R 3.6.0](https://img.shields.io/badge/R-3.6.0-green.svg)](https://www.r-project.org/)
[![Gunzip](https://img.shields.io/badge/Gunzip-1.6-green.svg)](https://www.gzip.org/)

[![Git](https://forthebadge.com/images/badges/uses-git.svg)](https://git-scm.com/)
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

<br>

## Step 1 - Project initialization and OmegaPlus downloading <a name="step1"></a>
To detect evidence for positive selection, we are going to use OmegaPlus. Information and download links for OmegaPlus can be found here: 
1. [http://www.exelixis-lab.org/software.html](http://www.exelixis-lab.org/software.html)
2. [https://github.com/alachins/omegaplus](https://github.com/alachins/omegaplus)

The first step should be to create a directory with your project name. Then, download and install OmegaPlus inside this directory.


```console
$ mkdir your-project-name
$ cd your-project-name/
$ git clone https://github.com/alachins/omegaplus.git
$ cd omegaplus/
$ ./compile_rename_ALL.sh
$ cd ..
```

After the sequence of commands, you have successfully installed OmegaPlus and you are ready to move to the next step.

<br>

## Step 2 - Preparation of the required data <a name="step2"></a>

#### Step 2.1 - ERV Insertions Information <a name="step21"></a>
The group of individuals and the positions, that we are going to analyse, are defined in a VCF format file. 

This file is available in this repository, in directory "SupportData" and we are going to use it in the next steps.

<code>Copy this vcf file to your "your-project-name" directory.</code>

<br>

#### Step 2.2 - Samples extraction from vcf file <a name="step22"></a>
We will use the vcf file, that was mentioned above, to extract lists of samples.

In our case, we are dealing with just two insertions. So, we are going to create two files for each insertion. One file containing a list of sample names that are genotyped with 0/0 (0|0) and one file with a list of sample names that are genotyped with 1/1 (1|1).

For this procedure, we are going to use a python script, that is available inside this repository. Place VCF-SamplesListCreator folder inside your working directory.

```console
$ python VCF-SamplesListCreator/VCFSamplesListCreator.py -v ERVtest.vcf
```

This command will create a bunch of files in our main directory. The files containing the samples that are genotyped with 0/1 are useless, for this research. Our next steps are to remove them and move the rest files to a separate directory, named <code>sampleLists</code>, in order to keep our main directory organized. 

```console
$ rm *.01.out
$ mkdir sampleLists
$ mv *.out sampleLists/
```

Now inside <code>sampleLists</code> directory, there are four files:

1. ERVtest.1.111802592.00.out
2. ERVtest.1.111802592.11.out
3. ERVtest.12.44313657.00.out
4. ERVtest.12.44313657.11.out

These files contain lists of samples that are genotyped with <code>0/0</code> or <code>1/1</code> for insertions in <code>chr1:111802592</code> and <code>chr12:44313657</code> respectively.

**NOTE!**  The files above, will be in this repository in the directory <code>SupportData/sampleLists/</code>

<br>

#### Step 2.3 - Grid points selection <a name="step23"></a>
For this example, we want to apply OmegaPlus in a specific area around each insertion.

There are two insertions, <code>chr1:111802592</code> and <code>chr12:44313657</code> and we will create 101 equally distributed points, including the insertion position, in a 500Kb space before and after each insertion.

In chromosome 1, we want to do the analysis in 101 points, with a distance of 5000bp and the middle point to be 111802592. So starting point should be <code>middle_point-(100/2)*distance=111552592</code> and ending point should be equal to <code>middle_point+(100/2)*distance=112052592</code>.  We use 100 in this equation, to exclude the middle point and 100/2 to take the half points before and the half points after the middle point.


In chromosome 12, we want to do the analysis in 101 points, with a distance of 5000bp and the middle point to be 44313657. The same way as above, we calculate starting and ending point of our grid points.

For our needs above, we will run the following commands and make use of an another script, I have written in python.

```console
$ git clone https://github.com/kutsukos/GridFileCreator.git
$ python GridFileCreator/GridFileCreator.py -c 1 -s 111552592 -e 112052592 -d 5000
$ python GridFileCreator/GridFileCreator.py -c 12 -s 44063657 -e 44563657 -d 5000
$ mkdir gridLists
$ mv points.* gridLists/
```


Done! Now inside <code>gridLists</code> directory, there are two files containing the list of points that we are interested.

**NOTE!** The files above, will be at this repository in the directory <code>SupportData/gridLists/</code>

<br>

#### Step 2.4 - Files downloading for analysis <a name="step24"></a>
For this example-workflow, we want to run this process on chromosome 1 and chromosome 12 vcf files from 1000 genome project - [http://www.internationalgenome.org/data](http://www.internationalgenome.org/data)

```console
$ mkdir vcfFiles
$ wget ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
$ gunzip -k ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
$ wget ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr12.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
$ gunzip -k ALL.chr12.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
$ mv ALL.* vcfFiles/
```

<br>

## Step 3 - Preparing OmegaPlus commands <a name="step3"></a>
We have just 4 runs, for this example, to execute, but in other cases, there can be more. So we developed OmegaCC python script in order to create a list of commands. Please place OmegaCC python script inside the main working directory.

In order to run OmegaCC, a tab-delimited file that, will contain all the necessary information for creating the commands and to define some options, is needed. 

**NOTE!** An example tab-delimited  file, will be in this repository in the directory SupportData/ named as <code>testproject.tab</code>

This file contains 6 fixed fields per line. All data lines are tab-delimited. Fixed fields are:
1. chr - an identifier to the chromosome to be scanned
2. position - the position of the insertion
3. input data filepath - the path to the vcf/bam file, that is going to be used for applying OmegaPlus.
4. grid points filepath - the path to the file containing the grid points
5. sample list filepath - the path to the file containing the samples' list
6. samples type - the type of samples, contained in file above. [00/11]

In case, you do not want to use grid file or sample list, fill the corresponding field with a dot (“.”).
In our case, we will use both of those options.

OmegaCC need also a few arguments:
1. -i | A tab-delimited file with some basic information for the run
2. -t | The number of threads to be used in  executing OmegaPlus
2. -d | Minimum window. For more info, please read OmegaPlus Manual
3. -u | Maximum window. For more info, please read OmegaPlus Manual
4. -s | Minimum SNPs. For more info, please read OmegaPlus Manual
5. -g | Grid. For more info, please read OmegaPlus Manual. In case there is a grid file used, this option is ignored
6. -O | Flag to create commands for running OmegaPlus with vcf files as input

We will choose <code>2</code> threads, <code>1000</code> as minimum window, <code>50000</code> as maximum window, <code>5</code> as minimum SNPs and <code>420</code> as grid. The grid option will be ignored, because we use a grid file.


```console
$ python OmegaCC.py -O -t 2 -d 1000 -u 50000 -s 5 -g 420 -i testproject.tab
$ chmod +x testproject.omega.cmd
```

<br>

## Step 4 - Executing OmegaPlus commands <a name="step4"></a>
The commands are written in <code>testproject.omega.cmd</code> file. The next step is to just execute this file, since it is already executable.

**NOTE!** In case, where this file has too many commands, there are ways to run these commands in parallel.

Now, we have just 4 commands to run, so there is no need to hurry. :D

```console
$ ./testproject.omega.cmd
$ mkdir omegaplusResults
$ mv *run omegaplusResults/
```

The results from OmegaPlus execution are inside <code>omegaplusResults/</code> directory.

<br>

## **Ιmportant Note!**
By successfully executing the steps above, we have actually completed detection of selective sweeps using OmegaPlus. The steps below are written for the "Detecting positive selection on ERV insertions in the human genome" project and what these steps describe is how to create control runs in order to define thresholds for each insertion's results and how to visually make conclusions.

<br>

## Step 5 - Control runs <a name="step5"></a>
In order to have a more clear view of the results, we need some control runs to define threshold for each insertion's OmegaPlus results. 

In our case, we want to see how the values range in 500Kb areas of the genome, where there are no ERVs insertions, areas without any reference transposable elements (LTRs, SINEs and LINEs).

We used <code>RepeatMasker</code> with <code>Dfam2.0</code> and <code>RepBaseRepeat MaskerEdition 20170127</code> libraries on <code>GRCh37/hg19</code> human genome reference, to get the positions of reference transposable elements. This procedure produced four files. A file with alignments of the query with the matching repeats, the human genome in which all recognized interspersed or simple repeats have been masked, a table annotating the masked sequences and a table summarizing the repeat content of the query sequence.
<br>The outputs of RepeatMasker can be found here <code>https://figshare.com/articles/GRCh37_hg19_RepeatMasker/7851005/1</code> .

Regions without any reference transposable elements, were discovered using a script on RepeatMasker's results, while centromeres and telomeres were excluded manually.

In <code>https://github.com/kutsukos/kutsukos2019SupplementaryData</code>, you can access all control regions, that was discovered at the procedure explained above.

Then, OmegaPlus will be applied on 350 (500Kb) subregions of those regions for each insertion's sample list.

Finally, the 95% percentile of the maximum likelihoods values will be used as thresholds, which will help us to infer which insertions have evidence for selection, visually.

For this example, we are going to use a few of those areas, just to show how the workflow worked for all of those. 
The files, we are going to use as grid points for the control runs are inside <code>gridListsCTRL</code> directory.

<br>

## Step 6 - Preparation of the required data for control runs <a name="step6"></a>

#### Step 6.1 - Files downloading for analysis <a name="step61"></a>
Lets say that, except chromosome 1 and 12, we have areas without ERVs insertions in chromosome 21 and 18. In fact, we do not have any areas, to satisfy our criteria, in chromosome 12.

```console
$ wget ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr18.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
$ gunzip -k ALL.chr18.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
$ wget ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr21.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
$ gunzip -k ALL.chr21.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
$ mv ALL.* vcfFiles/
```
<br>

#### Step 6.2 - Grid points selection REMINDER! <a name="step62"></a>
The files, we are going to use as grid points for the control runs are inside <code>gridListsCTRL</code> directory

<br>

## Step 7 - Preparing OmegaPlus control commands <a name="step7"></a>
For this step, we will use again, <code>OmegaCC</code> python script, you can find inside this repository, to create the commands. The script, in this case, needs the tab-delimited file with some mandatory information , we have already created and a few more arguments, that I am going to explain below.

**NOTE!** All those files, can be found in <code>SupportData/</code>. Reach them to understand the format and the content of those files.

This file contains 6 fixed fields per line. All data lines are tab-delimited. Fixed fields are:
1. chr - an identifier to the chromosome to be scanned
2. position - the position of the insertion
3. input data filepath - the path to the vcf/bam file, that is going to be used for applying OmegaPlus.
4. grid points filepath - the path to the file containing the grid points
5. sample list filepath - the path to the file containing the samples' list
6. samples type - the type of samples, contained in file above. [00/11]

OmegaCC need also a few arguments:
1. -i | A tab-delimited file with some basic information for the run
2. -t | The number of threads to be used in  executing OmegaPlus
2. -d | Minimum window. For more info, please read OmegaPlus Manual
3. -u | Maximum window. For more info, please read OmegaPlus Manual
4. -s | Minimum SNPs. For more info, please read OmegaPlus Manual
5. -g | Grid. For more info, please read OmegaPlus Manual. In case there is a grid file used, this option is ignored
6. -C | To create commands for running OmegaPlus to output osf files
7. -p | a file containing a list of all grid point files
8. -P | path where the control points are
9. -V | the path where the vcf files are stored



For our example, we will choose <code>2</code> threads, <code>1000</code> as minimum window, <code>50000</code> as maximum window, <code>5</code> as minimum SNPs and <code>420</code> as grid.


```console
$ python OmegaCC.py -C -t 2 -d 1000 -u 50000 -s 5 -g 420 -i testproject.tab -p gridListsCTRL/ctrlpoints.list -P gridListsCTRL/ -V vcfFiles/
$ chmod +x testproject.omega.ctrl.cmd
```


This command will create a file <code>testproject.omegactrl.cmd</code> with the commands that we will need to execute in order to get to the next stage of this analysis.

<br>

## Step 8 - Executing OmegaPlus control commands<a name="step8"></a>
We have many control areas in the same chromosomes and it will take us long time to execute the analysis in all of them. In such cases, there are ways to run multiple commands in parallel. We are not going to do this.
```console
$ chmod +x testproject.omegactrl.cmd
$ ./testproject.omegactrl.cmd
$ mkdir omegaCTRLResults
$ mv *.run omegaCTRLResults/
```

<br>

## Step 9 - Visualization of OmegaPlus results [optional] <a name="step9"></a>
The visualization of our results, will make easier to infer evidence for positive selection.
Otherwise, you can develop a script, that will define thresholds from the control runs and then these thresholds will define which insertions have evidence for positive selection.

We chose to calculate and draw the thresholds on the OmegaPlus results plots, using a script in R.

**NOTE!** You can find this script, in this repository. If you have experience in R, it will be easy to edit this script and bring it to your feet! Also, in [step5](#step5) we had explained, how the thresholds will be defined, in this script. Take a look there, to understand more the whole procedure.



OmegaPlot.R script need 4 arguments to run. The first two are files, we created before in order to create the commands for running OmegaPlus.

The last two arguments are the paths, first for the control results and second for the main OmegaPlus results. So the command is the following...

```console
$ Rscript OmegaPlot.R testproject.tab gridListsCTRL/ctrlpoints.list omegaCTRLResults/ omegaplusResults/
```

This script creates a pdf file named "omegaplus.plot.pdf", that contains the plots we wanted to create.

Insertions' plots with points that exceed the threshold are considered to have evidence for positive selection.

<br>

## CITATIONS <a name="cite"></a>
1. Alachiotis, N., Stamatakis, A., & Pavlidis, P. (2012). OmegaPlus: a scalable tool for rapid detection of selective sweeps in whole-genome datasets. Bioinformatics, 28(17), 2274-2275.

2. Smit, AFA and Hubley, R and Green, P. RepeatMasker Open-4.0. 2013--2015 [http://www.repeatmasker.org](http://www.repeatmasker.org)

3. Hubley, Robert, et al. "The Dfam database of repetitive DNA families." Nucleic acids research 44.D1 (2015): D81-D89.

4. Bao, Weidong, Kenji K. Kojima, and Oleksiy Kohany. "Repbase Update, a database of repetitive elements in eukaryotic genomes." Mobile Dna 6.1 (2015): 11.

5. Koutsoukos, I., Pavlidis, P.: GRCh37/hg19 RepeatMasker, [https://figshare.com/articles/GRCh37_hg19_RepeatMasker/7851005/1](https://figshare.com/articles/GRCh37_hg19_RepeatMasker/7851005/1), (2019)

## VERSION CHANGELOG <a name="version"></a>
<pre>
-2 - CURRENT
   + A more specialized workflow for this project
   + One python script to create commands for OmegaPlus command creator
-2.1 
   + Comments added in python script
</pre>


## Contact <a name="contact"></a>
Contact me at <code>skarisg@gmail.com</code> or <code>ioannis.kutsukos@gmail.com</code> for reporting bugs or anything else! :)