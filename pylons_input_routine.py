import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import *
import subprocess
def set_height(height, points):
    n_height = [int(height * 0.1)]

    for i in range(1, points-1):
        n_height.append((height * 0.2 + n_height[i - 1]).astype(int))

    n_height.append((height * 0.1 + n_height[-1]).astype(int))
    print(n_height)
    return n_height


def set_text_geom(n_height):
    n_height = list(map(str, n_height))
    geometry_dis = ["Top	0.	0.	" + n_height[-1] + ".	structural\n",
                    "Basea	0.	0.	" + n_height[0] + ".	structural\n",
                    "Baseb	0.	0.	" + n_height[1]+ ".	structural\n",
                    "Basec	0.	0.	" + n_height[2] + ".	structural\n",
                    "Based	0.	0.	" + n_height[3] + ".	structural\n",
                    "Basee	0.	0.	" + n_height[4] + ".	structural\n"]
    return geometry_dis


def set_text_acc(signalAcc, signalDur, signalLen, signalDT,factor, pgv_factor):
    load_acc = []
    stage_acc = []
    for acc in range(len(signalAcc)):
        load_acc.append(
            "Dynamic Time-history Load	Base	x	acceleration	" + str(int(1000*factor*pgv_factor[acc])) + ".	" + signalAcc[acc] + "\n")
        stage_acc.append("0.0	"+ str(signalDur[acc]) +"	"+ str(signalLen[acc]) + "	"+ str(signalDT[acc]) + "\n")
    return load_acc, stage_acc


def replace_text(input_file, name_output_file, geometry_dis, uload_acc,ustage_acc, output_directory) :
    file = open(input_file, "r")
    list_of_lines = file.readlines()

    for changed_line in range(41, 47):
        list_of_lines[changed_line] = geometry_dis[changed_line - 41]
    list_of_lines[95] = uload_acc
    list_of_lines[100] = ustage_acc
    file = open(os.path.join(output_directory, name_output_file), "w")
    file.writelines(list_of_lines)
    file.close()


def generate_input_seismofiles(signalAcc, signalDur, signalLen, signalDT, pylon_lengths, input_file, output_file, output_directory, factor, pgv_factor):
    load_acc, stage_acc = set_text_acc(signalAcc, signalDur, signalLen, signalDT, factor, pgv_factor)
    plengths = list(map(str, (pylon_lengths / 1000).astype(int)))

    for pylon_i in range(len(pylon_lengths)):
        n_height = set_height(pylon_lengths[pylon_i], 6)
        geometry_dis = set_text_geom(n_height)
        for acc_i in range(len(load_acc)):
            seismo_input_file="P" + plengths[pylon_i] + "L_" +signalAcc[acc_i]+"_" + str(int(factor*10)) + output_file
            replace_text(input_file, seismo_input_file, geometry_dis, load_acc[acc_i], stage_acc[acc_i],output_directory)


def batch_run_files(input_seismo_file):
    command_exe ="D:\Outils\SStruct_Engine_v5_2.exe"+ " "+ input_seismo_file
    wholecmd="'"+'cmd /k '+ '{'+command_exe+'}'+"'"
    print(command_exe)
    os.system(command_exe )


def getting_info_file(input_file):  # INPUTFILE IS FILENAMES[i]
    file = open(input_file, "r")
    list_of_lines = file.readlines()
    file.close()
    return list_of_lines


def extracting_results_file(list_of_lines):
    # Declaring variables to extract from file
    time = []  # Time variable
    # CONTX = []  # Displacement of the control node
    CONTR = []  # Rotation of the control node
    # DRIFT = []  # Structural drift
    CURVZaS1 = []  # Curvature of the pylon at the base a of the structure
    CURVZaS2 = []  # Curvature of the pylon at the base a of the structure
    CURVZbS1 = []  # Curvature of the pylon at the base b  of the structure
    CURVZbS2 = []  # Curvature of the pylon at the base b  of the structure
    CURVZcS1 = []  # Curvature of the pylon at the base b  of the structure
    CURVZcS2 = []  # Curvature of the pylon at the base  c of the structure.
    DEPLX_O = []  # Horizontal displacement at the base of the structure
    DEPLX_H = []  # Horizontal displacement at the top of the structure
    DEPLZ_O = []  # Vertical displacement at the base of the structure
    DEPLZ_H = []  # Vertical displacement at the top of the structure
    ROTAZ_H = []  # Rotation at the top of the structure
    FORCX = []  # Horizontal reaction at the base
    FORCZ = []  # Vertical reaction at the base
    MOMEN_S = []  # Moment at the base of the structure
    relaHDisp = []
    relaVDisp = []
    SStrain_max_PLaS1 = []
    SStress_max_PLaS1 = []
    SStrain_min_PLaS1 = []
    SStress_min_PLaS1 = []
    CStrain_max_PLaS1 = []
    CStress_max_PLaS1 = []
    CStrain_min_PLaS1 = []
    CStress_min_PLaS1 = []
    SStrain_max_PLcS1 = []
    SStress_max_PLcS1 = []
    CStrain_max_PLcS1 = []
    CStress_max_PLcS1 = []
    outputNumber = []  # Output number
    element = 0
    count = 0
    for line in range(len(list_of_lines)):
        if list_of_lines[line] == ' Output-No.       Time\n':
            count = count + 1
    node_loc_displ = np.empty((7, count), dtype=object)
    # Reading and saving results
    for line in range(len(list_of_lines)):
        if list_of_lines[line] == ' Output-No.       Time\n':
            element = element + 1
            getline = list_of_lines[line + 1]
            outputNumber.append(getline.split()[0])
            time.append(float(getline.split()[1]))
            # FORCES AT THE BASE
            getline = list_of_lines[line + 5]
            FORCX.append(float(getline.split()[1]))
            FORCZ.append(float(getline.split()[3]))
            MOMEN_S.append(float(getline.split()[5]))
            # DISPLACEMENTS AT THE BASE
            getline = list_of_lines[line + 10]
            DEPLX_O.append(float(getline.split()[1]))
            DEPLZ_O.append(float(getline.split()[3]))
            # DISPLACEMENTS AT THE TOP OF THE STRUCTURE
            getline = list_of_lines[line + 11]
            DEPLX_H.append(float(getline.split()[1]))
            DEPLZ_H.append(float(getline.split()[3]))
            ROTAZ_H.append(float(getline.split()[5]))
            # CURVATURES
            getline = list_of_lines[line + 56]
            CURVZaS1.append(float(getline.split()[1]))
            CURVZaS2.append(float(getline.split()[3]))
            getline = list_of_lines[line + 57]
            CURVZbS1.append(float(getline.split()[1]))
            CURVZbS2.append(float(getline.split()[3]))
            getline = list_of_lines[line + 58]
            CURVZcS1.append(float(getline.split()[1]))
            CURVZcS2.append(float(getline.split()[3]))

            # DEPLACEMENTS RELATIFS
            getline = list_of_lines[line + 43]
            CONTR.append(float(getline.split()[4]))
            relaHDisp.append((DEPLX_H[element - 1] - DEPLX_O[element - 1]))
            relaVDisp.append((DEPLZ_H[element - 1] - DEPLZ_O[element - 1]))
            # CONCRETE AND STEEL STRESS AND STRAINS
            getline = list_of_lines[line + 85]
            SStrain_max_PLaS1.append(float(getline.split()[5]))
            SStress_max_PLaS1.append(float(getline.split()[6]))
            SStrain_min_PLaS1.append(float(getline.split()[3]))
            SStress_min_PLaS1.append(float(getline.split()[4]))
            getline = list_of_lines[line + 86]
            CStrain_max_PLaS1.append(float(getline.split()[3]))
            CStress_max_PLaS1.append(float(getline.split()[4]))
            CStrain_min_PLaS1.append(float(getline.split()[1]))
            CStress_min_PLaS1.append(float(getline.split()[2]))
            getline = list_of_lines[line + 97]
            SStrain_max_PLcS1.append(float(getline.split()[5]))
            SStress_max_PLcS1.append(float(getline.split()[6]))
            getline = list_of_lines[line + 98]
            CStrain_max_PLcS1.append(float(getline.split()[3]))
            CStress_max_PLcS1.append(float(getline.split()[4]))

            for element_loc in range(7):
                if element_loc == 0 :
                    node_loc_displ[element_loc, element - 1] = 0
                elif element_loc > 0 :
                    getline = list_of_lines[line + 41 + 2 * (element_loc-1)]
                    node_loc_displ[element_loc, element - 1] = float(getline.split()[2])

    return time, DEPLX_O, DEPLX_H, relaVDisp, ROTAZ_H, FORCZ, FORCX, MOMEN_S, CURVZaS2, CURVZbS1, CURVZaS1, CURVZbS2, CURVZcS1, CURVZcS2, CONTR, relaHDisp, node_loc_displ, SStrain_min_PLaS1, SStrain_max_PLaS1, CStrain_max_PLaS1, SStress_min_PLaS1, SStress_max_PLaS1, CStress_max_PLaS1, CStrain_min_PLaS1, CStress_min_PLaS1

def table_max_file(signal, case, factor, pgv, relaHDisp, relaVDisp, MOMEN_S,CURVZaS1, CStrain_max_PLaS1, CStrain_min_PLaS1, SStrain_max_PLaS1, SStrain_min_PLaS1, ROTAZ_H, DEPLX_O):
    ky = 0.00000036  # ky= 1.8*35/(30000*0.002*2925) 1/mm
    max_relaHDisp = max(abs(max(relaHDisp)), abs(min(relaHDisp))) / 1000 #m
    max_CDR = max(abs(max(CURVZaS1)), abs(min(CURVZaS1))) / ky
    max_MOMEN_S = max(abs(max(MOMEN_S)), abs(min(MOMEN_S)))/1000000000 # MN m
    max_CStrain = max(CStrain_max_PLaS1)
    min_CStrain = min(CStrain_min_PLaS1)
    max_SStrain = max(SStrain_max_PLaS1)
    min_SStrain = min(SStrain_min_PLaS1)
    max_ROTAZ_H = max(abs(max(ROTAZ_H )), abs(min(ROTAZ_H ))) # rad
    max_DEPLX_O = max(abs(max(DEPLX_O)), abs(min(DEPLX_O)))/1000  # m
    max_relaVDisp = max(abs(max(relaVDisp)), abs(min(relaVDisp)))/1000 #m
    #Creating list-table
    table_line = signal + " " + case + " " + factor + " " + pgv + " " + str('%.4f'%max_relaHDisp) + " " + str('%.4f'%max_DEPLX_O) + " " +  str('%.4f'%max_ROTAZ_H) + " " + str('%.4f'%max_ROTAZ_H)+ " " + str('%.4f'%max_CDR)+ " " + str('%.4f'%max_relaVDisp)+" " + str('%.2f'%max_MOMEN_S)+ " " + str('%.4f'%max_CStrain) + " " + str('%.4f'%min_CStrain) + " " + str('%.4f'%max_SStrain)+ " " + str('%.4f'%min_SStrain) +"\n"
    return (table_line)

def writing_textfile_results(output_directory, namefile, table):
    file = open(os.path.join(output_directory, namefile), "w")
    file.writelines(table)
    file.close()

def plotting_results(analysis_name, time, relaVDisp, FORCZ, FORCX, MOMEN_S, CURVZaS2, CURVZbS1, CURVZaS1, CURVZbS2, CURVZcS1, CURVZcS2, CONTR, relaHDisp, node_loc_displ, SStrain_min_PLaS1, SStrain_max_PLaS1, CStrain_max_PLaS1, SStress_min_PLaS1, SStress_max_PLaS1, CStress_max_PLaS1, CStrain_min_PLaS1, CStress_min_PLaS1):
    ##------------------------------------------------------------------------------------------- Plotting results
    rc('figure', figsize=(11.69, 8.27))
    # Time Histories
    plt.clf()
    plt.plot(time, relaHDisp, 'b-')
    plt.grid(True)
    plt.gca().xaxis.grid(True, which='minor')
    plt.gca().yaxis.grid(True, which='minor')
    plt.xlabel('Time [s]')
    plt.ylabel('Top horizontal displacement [mm]')
    plt.savefig(analysis_name + 'a_DeplX_TH.png')

    plt.clf()
    plt.plot(time, relaVDisp, 'b-')
    plt.grid(True)
    plt.gca().xaxis.grid(True, which='minor')
    plt.gca().yaxis.grid(True, which='minor')
    plt.xlabel('Time [s]')
    plt.ylabel('Top vertical displacement [mm]')
    plt.savefig(analysis_name +'b_DeplZ_TH.png')

    # Steel Strain - stress
    plt.clf()
    plt.plot(SStrain_max_PLaS1, SStress_max_PLaS1, 'k-')
    plt.plot(SStrain_min_PLaS1, SStress_min_PLaS1, 'g-')

    plt.grid(True)
    plt.gca().xaxis.grid(True, which='minor')
    plt.gca().yaxis.grid(True, which='minor')
    plt.xlabel('Strain [-]')
    plt.ylabel('Stress [MPa]')
    plt.savefig(analysis_name +'c_SteelStressStrain.png')
    # Concrete Strain - stress
    plt.clf()
    plt.plot(CStrain_max_PLaS1, CStress_max_PLaS1, '-k')
    plt.plot(CStrain_min_PLaS1, CStress_min_PLaS1, '-g')
    plt.grid(True)
    plt.gca().xaxis.grid(True, which='minor')
    plt.gca().yaxis.grid(True, which='minor')
    plt.limits = [min(CStrain_min_PLaS1), 0.0003, min(CStress_min_PLaS1), max(CStress_max_PLaS1)]
    plt.xlabel('Strain [-]')
    plt.ylabel('Stress [MPa]')
    plt.savefig(analysis_name +'d1_ConcreteStressStrain.png')

    # Concrete Strain - stress
    plt.clf()
    plt.plot(CStrain_max_PLaS1, CStress_max_PLaS1, '-k')
    plt.plot(CStrain_min_PLaS1, CStress_min_PLaS1, '-g')
    plt.grid(True)
    plt.gca().xaxis.grid(True, which='minor')
    plt.gca().yaxis.grid(True, which='minor')
    plt.xlabel('Strain [-]')
    plt.ylabel('Stress [MPa]')
    plt.savefig(analysis_name +'d2_ConcreteStressStrain.png')

    plt.clf()
    # Vertical force- Vertical displacement
    plt.plot(relaVDisp, FORCZ, 'b-')
    plt.grid(True)
    plt.gca().xaxis.grid(True, which='minor')
    plt.gca().yaxis.grid(True, which='minor')
    plt.xlabel('Top vertical displacement [mm]')
    plt.ylabel('Vertical reaction force [MN]')
    plt.savefig(analysis_name +'e_TopVerticalDisp_VForce.png')

    # Horizontal force - Horizontal displacement
    plt.clf()
    plt.plot(relaHDisp, FORCX, 'b-')
    plt.grid(True)
    plt.gca().xaxis.grid(True, which='minor')
    plt.gca().yaxis.grid(True, which='minor')
    plt.xlabel('Top horizontal displacement [mm]')
    plt.ylabel('Horizontal reaction force [MN]')
    plt.savefig(analysis_name +'f_TopHorizontalDisp_HForce.png')

    # Moment - Horizontal displacement
    plt.clf()
    plt.plot(relaHDisp, MOMEN_S, 'b-')
    plt.grid(True)
    plt.gca().xaxis.grid(True, which='minor')
    plt.gca().yaxis.grid(True, which='minor')
    plt.xlabel('Top horizontal displacement [mm]')
    plt.ylabel('Reaction moment [MNmm]')
    plt.savefig(analysis_name +'g_Moment_TopHorizontalDisp.png')

    # Moment - Rotation
    plt.clf()
    plt.plot(CONTR, MOMEN_S, 'r-', label='Base')
    plt.grid(True)
    plt.gca().xaxis.grid(True, which='minor')
    plt.gca().yaxis.grid(True, which='minor')
    # gca().legend()
    plt.xlabel('Rotation at PLa point A [rad]')
    plt.ylabel('Reaction moment [MNmm]')
    plt.savefig(analysis_name +'h_BaseMomentvsRotationCONTb.png')

    # Moment - Force
    plt.clf()
    plt.plot(FORCX, MOMEN_S, 'r-', label='Base')
    plt.grid(True)
    plt.gca().xaxis.grid(True, which='minor')
    plt.gca().yaxis.grid(True, which='minor')
    # gca().legend()
    plt.xlabel('Horizontal force at the base [N]')
    plt.ylabel('Moment at the base [MNmm]')
    plt.savefig(analysis_name +'i_BaseMomentvsHorizontalForce.png')

    # Moment - Displacement
    plt.clf()
    plt.plot(relaHDisp, MOMEN_S, 'r-', label='Base')
    plt.grid(True)
    plt.gca().xaxis.grid(True, which='minor')
    plt.gca().yaxis.grid(True, which='minor')
    # gca().legend()
    plt.xlabel('Top displacement [mm]')
    plt.ylabel('Moment at the base [MNmm]')
    plt.savefig(analysis_name +'j_BaseMomentvsHorizontalDisp.png')

    # Moment - Curvature
    plt.clf()
    plt.plot(CURVZaS1, MOMEN_S, 'r-', label='PLaS1')
    plt.plot(CURVZaS2, MOMEN_S, 'g-', label='PLaS2')
    plt.plot(CURVZbS1, MOMEN_S, 'b-', label='PLbS1')
    plt.plot(CURVZbS2, MOMEN_S, 'm-', label='PLbS2')
    plt.plot(CURVZcS1, MOMEN_S, 'k-', label='PLcS1')
    plt.plot(CURVZcS2, MOMEN_S, 'c-', label='PLcS2')
    plt.grid(True)
    plt.legend()
    plt.gca().xaxis.grid(True, which='minor')
    plt.gca().yaxis.grid(True, which='minor')
    plt.xlabel('Curvature [1/mm]')
    plt.ylabel('Moment at the base [MNmm]')
    plt.savefig(analysis_name +'k_BaseMomentvsCurvature.png')

    plt.clf()
    plt.plot(node_loc_displ, [0,0.021,0.142,0.34,0.54,0.74,0.92])
    plt.xlabel('Axial deformation dl [mm]')
    plt.ylabel('A-Gauss point location [x/L]')
    plt.savefig(analysis_name +'l_AxialDeformationdl_TH.png')


