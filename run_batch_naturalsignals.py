from pylons_input_routine_macro import *
import numpy as np
import os


#INPUT DATA
# THIS PROGRAM NEEDS FIVE ARRAYS: SIGNALACC: NAME OF SIGNALS ALREADY REGISTER ON THE BASE SEISMOSTRUCTURE FILE (EXTENSION .SPF)
# SIGNALDUR: THE SIGNAL DURATION IN SECONDS
# SIGNALLEN: THE SIGNAL LENGTH DATA POINTS OF THE TIME HISTORY SIGNAL
# SIGNALDT: TIME STEP IN SECONDS
# PYLON_LENGTHS: THE PYLON LENGTHS IN MM
signalAcc = [vector_name]
signalDur = [vector_duration]
signalLen = [vector_length]
signalDT = [vector_timedelta]
pylon_lengths = np.array([21000, 30000, 40000, 50000, 60000])
pgv_factor = np.array([vector_scale])  # PGV body waves=0.2 m/s

scale_factor = np.array([vector_factor])
factor = 1  #Default is 1

#SPECIFYING THE BASE .spf FILE (INPUT SEISMOSTRUCT FILES)
input_file = "./Base_Macroelement_batch.spf"

#SPECIFYING THE INPUT FILES INFO (INPUT SEISMOSTRUCT FILES)
end_output_file = "_SmallDisp_Macro.spf"

folder_output_file="c_SeismoMacroelement_InputFiles" #THE NAME OF THE FOLDER FOR INPUT FILES
output_directory= folder_output_file

#-----------------------------------------------END OF INPUT SECTION

#CREATING THE INPUT FILES FOLDER IF IT DOESNOT EXIST

if not os.path.exists(folder_output_file):
    os.mkdir(folder_output_file)

#GENERATING THE INPUT TEXT FILES FOR SEISMOSTRUCT
for ite_factor in range(len(scale_factor)):
    factor = scale_factor[ite_factor]
    generate_input_seismofiles(signalAcc, signalDur, signalLen, signalDT, pylon_lengths, input_file, end_output_file, output_directory, factor, pgv_factor) #UNCOMMENT IF NEED IT


#READING THE GENERATED INPUT .SPF FILES
from os import walk
filenames = next(walk(folder_output_file), (None, None, []))[2]  # [] if no file
print(filenames)

#RUNNING ALL CASES WITH SEISMOSTRUCT
for set_file in range(len(filenames)):
    seismo_file_name= filenames[set_file]
    print("Current simulation run with this input file:"+filenames[set_file])
    input_seismo_file = "C:\\Users\\carolina.franco\\Documents\\Carolina_LOCAL\\1_Modulate\\1_Computations\\C_PylonsModel\\pythonProjects\\c_SeismoMacroelement_InputFiles\\"+ seismo_file_name
    #input_seismo_file ="C:\\Users\\carolina.franco\\Documents\\Carolina_LOCAL\\1_Modulate\\1_Computations\\C_PylonsModel\\pythonProjects\\Pylon_Base.spf"
    batch_run_files(input_seismo_file)
