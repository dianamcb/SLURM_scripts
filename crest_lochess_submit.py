#!/usr/bin/python

# Author: Diana Marlen Castaneda Bagatella
# Description: This script can generate all the bash files (.sh) to run CREST calculations in SLURM for the Lochness cluster automaticly. 
# Run as: python crest_lochess_submit.py file.com number_of_days number_of_CPUs

import sys
import os

##############################################
# Email Notification Settings                #
#                                            #
# Set "send_email" to 1 and edit your email  #
# address to enable email notification       #
#                                            #
# email_options:                             #
#   begin, end, fail, or all                 #
#                                            #

send_email = 0
email_address = "UCID@njit.edu"
email_options = "all"

#                                            #
# End of Email Notification Settings         #
##############################################

l = len(sys.argv)
if l < 2:
   print('Usage: '+os.path.basename(sys.argv[0])+' filename.xyz ncpus(=8) walltime(=24)')
   sys.exit(1)

walltime = "24"
ncpus = 8

if l >= 4:
   walltime = sys.argv[3]

if l >= 3:
   ncpus = int(sys.argv[2])

def write_bash_file(bash_filename, crest_filename, filename):
    """
    Writes a bash file which is submitted to the queue. 
    bash_filename (string): name of the bash file to be created 
    crest_filename: crest.xyz input file
    """
    
    bash_file = open(bash_filename, "w")
    bash_file.write("#!/bin/bash -l\n")
    bash_file.write("#SBATCH -J "+crest_filename+'\n')
    bash_file.write("#SBATCH -o "+crest_filename+'.output\n')
    bash_file.write("#SBATCH -e "+crest_filename+'.output\n')
    bash_file.write("#SBATCH --nodes=1\n")
    bash_file.write("#SBATCH --ntasks=1\n")
    bash_file.write("#SBATCH --cpus-per-task="+str(ncpus)+'\n')
    bash_file.write("#SBATCH --mem-per-cpu=10G\n")
    bash_file.write("#SBATCH -p public\n")
    bash_file.write("#SBATCH -t "+str(walltime)+"-00:00:00\n")
    if send_email == 1:
       bash_file.write("#SBATCH --mail-user="+email_address+"\n")
       bash_file.write("#SBATCH --mail-type="+email_options+"\n")
    
    bash_file.write("module purge\n")
    bash_file.write("module load intel//19.1.0.166\n")    
    bash_file.write("module load xtb/6.3.0\n")
    bash_file.write("module load crest/2.10.2\n")
	
    bash_file.write(" crest "+filename+ " -T " +str(ncpus)+ "-g toluene --chrg 1 --copy --verbose >> " +results_filename+'.txt\n')
    bash_file.close()

def main():  #submits bash file to queue.
   
    filename = sys.argv[1] 
    g16_filename = filename.split('.')[0]
    bash_filename = crest_filename+'.sh'
    write_bash_file(bash_filename, crest_filename, filename)
    os.system('sbatch '+bash_filename)
  
if __name__ == "__main__":
  main()
