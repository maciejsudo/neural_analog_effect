import os
from PyLTSpice import SimCommander


def processing_data(raw_file, log_file):
    print("Handling the simulation data of %s, log file %s" % (raw_file, log_file))


def run_mult_sims(path,fs,bit_depth,base_rec_path,seq_tone,seq_level,seq_dist,path_to_asc,tran_time):
    sim_num =1
    for l in seq_level:
        for t in seq_tone:
            for d in seq_dist:

                #Execution Parameters:
                t_tok= int(t/1000)
                l_tok= int(l/1000)
                d_tok= int(d/1000)
                outputfilename = f"T{t_tok}k_L{l_tok}k_D{d_tok}k_fs{fs}_bd{bit_depth}_time{tran_time}s"

                print(f"* SIMULATION no. {sim_num} Output: {outputfilename} *")
                sim_num += 1

                LTC = SimCommander(path_to_asc)

                tran_param = f".tran {tran_time}s"
                options_param = ".options gmin=1e-10 abstol=1e-10 reltol=0.003"
                level_param = f".param level={l}"
                tone_param = f".param tone={t}"
                dist_param = f".param distortion={d}"

                level_2 = f"level={l}"
                tone_2 = f"tone={t}"
                dist_2 = f"distortion={d}"

                LTC.set_parameter("level",l)
                LTC.set_parameter("tone",t)
                LTC.set_parameter("distortion",d)




                #wavefile ="D:\neural_model\LTSpice_sims\database\raw_data4.wav" chan=1
                source_file = f"""wavefile ="{base_rec_path}" chan=1"""
                output_path1 = f""".wave "{path}\\input.wav" {bit_depth} {fs} V(out_input)"""
                output_path2 = f""".wave "{path}\\{outputfilename}-target.wav" {bit_depth} {fs} V(output)"""


                LTC.set_element_model('V1', source_file)



                if(os.path.isfile(path+'\input.wav')):
                    LTC.add_instructions(
                        "; Simulation settings",
                        tran_param,
                        output_path2,
                        #level_param,
                        #tone_param,
                        #dist_param,
                        options_param
                    )


                else:
                    LTC.add_instructions(
                        "; Simulation settings",
                        tran_param,
                        output_path1,
                        output_path2,
                        #level_param,
                        #tone_param,
                        #dist_param,
                        options_param
                    )
                LTC.run()
                LTC.wait_completion()
                # Sim Statistics
                print('Successful/Total Simulations: ' + str(LTC.okSim) + '/' + str(LTC.runno))
                LTC.reset_netlist()


base_recording_path =  f"""D:\\repos\MGR\\neural_analog_effect_database_gen\database\sources\originals\\raw_data4.wav"""
path_to_asc = f"""D:\\repos\MGR\\neural_analog_effect_database_gen\schematics\\test_v2.asc"""
parent_dir = "D:\\repos\MGR\\neural_analog_effect_database_gen\database\\targets\\time_test"


directory = "database_125"
path = os.path.join(parent_dir, directory)
#os.mkdir(path)

# 1,4000,8000,12000,16000 - nie zostało dopracowane!!
# seq_tone jest juz zrobione dla 20000 w calosci!!

seq_tone = [1]  #,2000,4000,6000,8000,10000,12000,14000] #max = 20k min =1
seq_level = [100000] #max = 100k min =1    #1,20000,40000,60000,80000,
seq_dist = [1,20000,40000,60000,80000,100000]  #max = 100k min =1
tran_time = 180 #180
sampling_rate = 44100
bit_depth = 16



run_mult_sims(path, sampling_rate,bit_depth,base_recording_path,seq_tone,seq_level,seq_dist,path_to_asc,tran_time)