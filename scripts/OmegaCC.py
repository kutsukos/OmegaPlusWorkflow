#!/usr/bin/python
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-i", "--input", dest="infile", help="a tab-delimited file with some basic information for the run", metavar="FILE")
parser.add_option("-t", "--threads", dest="nthreads", help="Number of threads to used for this analysis", metavar="FILE")
parser.add_option("-d", "--minwin", dest="nminwin", help="Minimum window. For more info, please read OmegaPlus Manual", metavar="FILE")
parser.add_option("-u", "--maxwin", dest="nmaxwin", help="Maximum window. For more info, please read OmegaPlus Manual", metavar="FILE")
parser.add_option("-s", "--minsnps", dest="nminsnps", help="Minimum SNPs. For more info, please read OmegaPlus Manual", metavar="FILE")
parser.add_option("-g", "--grid", dest="ngrid", help="Grid. For more info, please read OmegaPlus Manual. In case there is a grid file used, this option is ignored", metavar="FILE")
parser.add_option("-O", "--omega",action="store_true", dest="omegaflag", default=False,help="create commands for running OmegaPlus in default mode")
parser.add_option("-C", "--omegacontrol",action="store_true", dest="omegactrlflag", default=False,help="create commands for running OmegaPlus for control runs")

parser.add_option("-p", "--ctrlpointlist", dest="ctrlpointlist", help="a file containing a list of all grid point files", metavar="FILE")
parser.add_option("-P", "--ctrlpointspath", dest="ctrlpointspath", help="path where the control points are", metavar="NUM")
parser.add_option("-V", "--vcfpath", dest="vcfpath", help="the path where the vcf files are stored", metavar="NUM")

(options, args) = parser.parse_args()

input_file=options.infile



## args
OMEGAflag=options.omegaflag
OMEGACTRLflag=options.omegactrlflag
threads=options.nthreads
minwin=options.nminwin
maxwin=options.nmaxwin
minsnps=options.nminsnps
randomseed=" -seed " + str(13124203)
grid=options.ngrid

control_pointlist_path=options.ctrlpointspath
control_pointlist_filepath=options.ctrlpointlist
vcf_filepath=options.vcfpath
##

if(OMEGAflag+OMEGACTRLflag==1):
    if (OMEGAflag == 1):
        output_file=input_file.split(".tab")[0]+".omega.cmd"
    else:  #time to read the file with the control points
        output_file=input_file.split(".tab")[0]+".omegactrl.cmd"
        file2 = open(control_pointlist_filepath, "r"); DB=[];   # A list of the grifFiles that are going to be used
        for line in file2:
            newline=line.split("\n")[0]         # Removing the newline symbol from the line
            DB.append(control_pointlist_path+"/"+newline)
        file2.close()

    file = open(input_file, "r")
    chr='';pos='';
    cmds=[]

    for line in file:
        newlineSHIET=line.split("\n")
        values=newlineSHIET[0].split('\t')
        chr=values[0]
        pos=values[1]
        vcffile=values[2]
        
        samplefile_option=""
        samplestype=values[5];
        
        if (values[4]!='.') :
            samplefile_option=" -sampleList " +values[4]

        runID = " -name chr" + chr + "." + pos+"."+samplestype+".run"
        minimum_snps_option= " -minsnps "+minsnps
        input_option= " -input " + vcffile
        grid_option = " -grid " + grid;
        threads_option= " -threads " + threads
        max_min_windows=" -minwin " + minwin + " -maxwin " + maxwin
        
        gridfile=""
        if(OMEGAflag==1):
            runID = " -name chr" + chr + "." + pos+"."+samplestype+".run"
            if (values[3]!='.') :
                gridfile=" -gridFile " +values[3]
            cmds.append(
            "omegaplus/OmegaPlus-M"+ runID + input_option  + minimum_snps_option + gridfile + samplefile_option + grid_option + threads_option + max_min_windows  + randomseed)
        else:
            for ctrlpointsfile in DB:
                gridfile=" -gridFile " + ctrlpointsfile
                runID = " -name chr" + chr + "." + pos+"." + samplestype+".at."+ctrlpointsfile.split("ctrl.")[1]+".run"

                ctrlvcf=ctrlpointsfile.split("chr")[1].split(".")[0]

                input_option= " -input " + vcf_filepath + "ALL.chr"+ctrlvcf+".phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf"
                
                cmds.append(
            "omegaplus/OmegaPlus-M"+ runID + input_option  + minimum_snps_option + gridfile + samplefile_option + grid_option + threads_option + max_min_windows  + randomseed)

        

    
file.close()
file2 = open(output_file, "w")
for item in cmds:
    file2.write(str(item) + "\n")
file2.close()
