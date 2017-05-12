
import sys
import random

#Generates new config files and runs algorithm
#Call with args[1] equal to number of configs
#Ex: python3 gen_config_and_run.py 10


# Example of file
# {
#     "_use_": "Use this config file with the ttp_ea.py script",
    
#     "development": true,
#     "plot_generations": true,
#     "runs": 1,

#     "tsp": {
#         "mutation": {
#             "probability": 0.02
#         },
#         "crossover": {
#             "probability": 0.8
#         }
#     },

#     "kp": {
#         "mutation": {
#             "probability": 0.01
#         },
#         "crossover": {
#             "probability": 0.8
#         }
#     },

#     "tournament_size": 5,
#     "elite_percentage": 0.1,
#     "number_generations": 100,
#     "size_population": 100
# }





def generateConfigFiles(number_of_files):


    for i in range(0,number_of_files):
        config = open("gen_configs_ttp_ea/config_ttp_ea_" + str(i) + ".json","w");  


        tsp_mutation_probability = random.uniform(0.0, 1.0);
        tsp_crossover_probability = random.uniform(0.0, 1.0);
        kp_mutation_probability = random.uniform(0.0, 1.0);
        kp_crossover_probability = random.uniform(0.0, 1.0);
        elite_percentage = random.uniform(0.0, 1.0);

        
        config.write('{\n');
        config.write('    "_use_": "Use this config file with the ttp_ea.py script",\n');
        config.write('    \n');
        config.write('    "development": true,\n');
        config.write('    "plot_generations": true,\n');
        config.write('    "runs\": 1,\n');
        config.write('    \n');
        config.write('    "tsp": {\n');
        config.write('        "mutation": {\n');
        config.write('            "probability": '+ str(tsp_mutation_probability) + '\n');
        config.write('        },\n');
        config.write('        "crossover": {\n');
        config.write('            "probability": '+ str(tsp_crossover_probability) + '\n');
        config.write('        }\n');
        config.write('    },\n');
        config.write('    \n');
        config.write('    "kp": {\n');
        config.write('        "mutation": {\n');
        config.write('            "probability": '+ str(kp_mutation_probability) + '\n');
        config.write('        },\n');
        config.write('        "crossover": {\n');
        config.write('            "probability": '+ str(kp_crossover_probability) + '\n');
        config.write('        }\n');
        config.write('    },\n');
        config.write('\n');
        config.write('    "tournament_size": 5,\n');
        config.write('    "elite_percentage": '+ str(elite_percentage) + ',\n');
        config.write('    "number_generations": 100,\n');
        config.write('    "size_population": 100\n');
        config.write('}\n');

        config.close();




if __name__ == "__main__":

    number_of_files = int(float(sys.argv[1]));
    generateConfigFiles(number_of_files);










