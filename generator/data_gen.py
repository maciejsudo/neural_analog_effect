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
                outputfilename = f"T{t_tok}k_L{l_tok}k_D{d_tok}k_fs{fs}_bd{bit_depth}_time{tran_time}s-target"

                print(f"* SIMULATION no. {sim_num} Output: {outputfilename} *")
                sim_num += 1

                LTC = SimCommander(path_to_asc)

                tran_param = f".tran {tran_time}s"
                options_param = ".options gmin=1e-10 abstol=1e-10 reltol=0.003"
                level_param = f".param level={l}"
                tone_param = f".param tone={t}"
                dist_param = f".param distortion={d}"


                #wavefile ="D:\neural_model\LTSpice_sims\database\raw_data4.wav" chan=1
                source_file = f"""wavefile ="{base_rec_path}" chan=1"""
                output_path1 = f""".wave "{path}\\data_in.wav" {bit_depth} {fs} V(guitar_input)"""
                output_path2 = f""".wave "{path}\\{outputfilename}.wav" {bit_depth} {fs} V(output)"""


                LTC.set_element_model('V1', source_file)

                if(os.path.isfile(path+'\data_in.wav')):
                    LTC.add_instructions(
                        "; Simulation settings",
                        tran_param,
                        output_path2,
                        level_param,
                        tone_param,
                        dist_param,
                        options_param
                    )
                else:
                    LTC.add_instructions(
                        "; Simulation settings",
                        tran_param,
                        output_path1,
                        output_path2,
                        level_param,
                        tone_param,
                        dist_param,
                        options_param
                    )
                LTC.run()
                LTC.wait_completion()
                # Sim Statistics
                print('Successful/Total Simulations: ' + str(LTC.okSim) + '/' + str(LTC.runno))
                LTC.reset_netlist()


base_recording_path =  f"""D:\MGR\\neural_analog_effect_database_gen\generator\database\\raw_data4.wav"""
path_to_asc = f"""D:\MGR\\neural_analog_effect_database_gen\generator\schematics\BOSS_DS1.asc"""
print(path_to_asc)
print(base_recording_path)

seq_tone = [1,2000,4000,6000,8000,10000,12000,14000] #max = 20k min =1
seq_level = [1000] #max = 100k min =1
seq_dist = [1000]  #max = 100k min =1
tran_time = 180 #180
sampling_rate = 44100
bit_depth = 16

directory = "test_exec_tone_0k_14k"
parent_dir = "D:\MGR\\neural_analog_effect_database_gen\generator\database"
path = os.path.join(parent_dir, directory)
os.mkdir(path)

run_mult_sims(path, sampling_rate,bit_depth,base_recording_path,seq_tone,seq_level,seq_dist,path_to_asc,tran_time)