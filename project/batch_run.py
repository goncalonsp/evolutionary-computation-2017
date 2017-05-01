import subprocess
import os

python_cmd = "python3"
program = "ttp.py"
config = "config.json"

subprocess.run([python_cmd, program, "instances" + os.path.sep + "a280_n279_bounded-strongly-corr_01.ttp", "-c", config])
subprocess.run([python_cmd, program, "instances" + os.path.sep + "a280_n1395_uncorr-similar-weights_05.ttp", "-c", config])
subprocess.run([python_cmd, program, "instances" + os.path.sep + "a280_n2790_uncorr_10.ttp", "-c", config])
subprocess.run([python_cmd, program, "instances" + os.path.sep + "fnl4461_n4460_bounded-strongly-corr_01.ttp", "-c", config])
subprocess.run([python_cmd, program, "instances" + os.path.sep + "fnl4461_n22300_uncorr-similar-weights_05.ttp", "-c", config])
subprocess.run([python_cmd, program, "instances" + os.path.sep + "fnl4461_n44600_uncorr_10.ttp", "-c", config])
