#!/usr/bin/python

# Author: Diana Marlen Castaneda Bagatella
# Description: This script can generate all the bash files (.sh) to run ORCA calculations in SLURM for the Lochness cluster automaticly. 
# Run as: python orca_lochness_submit.py file.com number_of_days number_of_CPUs

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
email_options = "end,fail"

#                                            #
# End of Email Notification Settings         #
##############################################

l = len(sys.argv)
if l < 2:
  print('Usage: '+os.path.basename(sys.argv[0])+' filename.com ncpus(=8) walltime(=24)')
  sys.exit(1)

walltime = "24"
ncpus = 8

if l >= 4:
  walltime = sys.argv[3]

if l >= 3:
  ncpus = int(sys.argv[2])

def write_bash_file(bash_filename, g16_filename, filename):
    """
    Writes a bash file which is submitted to the queue. 
    bash_filename (string): name of the bash file to be created 
    g16_filename: Gaussian 16 input file
    """
    
    bash_file = open(bash_filename, "w")
    bash_file.write("#!/bin/bash -l\n")
    bash_file.write("#SBATCH -J "+g16_filename+'\n')
    bash_file.write("#SBATCH -o "+g16_filename+'.output\n')
    bash_file.write("#SBATCH -e "+g16_filename+'.output\n')
    bash_file.write("#SBATCH --ntasks="+str(ncpus)+'\n')
    bash_file.write("#SBATCH --mem-per-cpu=10G\n")
    bash_file.write("#SBATCH -p public\n")
    bash_file.write("#SBATCH -t "+str(walltime)+":00:00\n")
    if send_email == 1:
      bash_file.write("#SBATCH --mail-user="+email_address+"\n")
      bash_file.write("#SBATCH --mail-type="+email_options+"\n")
    
    bash_file.write("module purge\n")
    bash_file.write("module use /opt/site/easybuild/modules/all/Core\n")
    bash_file.write("module load GCC/8.3.0 OpenMPI/3.1.4 ORCA/4.2.1\n")
    bash_file.write("/opt/site/easybuild/software/ORCA/4.2.1-gompi-2019b/orca "+filename+' > '+g16_filename+'.out\n')
    bash_file.close()

def main():  #submits bash file to queue.
   
    filename = sys.argv[1] 
    g16_filename = filename.split('.')[0]
    bash_filename = g16_filename+'.sh'
    write_bash_file(bash_filename, g16_filename, filename)
    os.system('sbatch '+bash_filename)
  
if __name__ == "__main__":
  main()
