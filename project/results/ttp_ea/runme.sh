#!/bin/bash
PROGRAM_CMD="python3"
PROGRAM="../../ttp_ea.py"
CONFIG_FILE="config.json"
LOCATION="../../instances"

declare -a instances=("a280_n279_bounded-strongly-corr_01" 
	"a280_n1395_uncorr-similar-weights_05" 
	"a280_n2790_uncorr_10")
	# "fnl4461_n4460_bounded-strongly-corr_01"
	# "fnl4461_n22300_uncorr-similar-weights_05"
	# "fnl4461_n44600_uncorr_10")

for instance in "${instances[@]}"
do
	echo "Starting $instance"
	$PROGRAM_CMD $PROGRAM $LOCATION/$instance.ttp -c $CONFIG_FILE -s $instance.png &> $instance.results &
done

for job in `jobs -p`
do
echo "Waiting for job $job to finish"
    wait $job || let "FAIL+=1"
done
echo $FAIL

for instance in "${instances[@]}"
do
	echo "Starting 30 run for $instance"
	$PROGRAM_CMD $PROGRAM $LOCATION/$instance.ttp -r 30 -c $CONFIG_FILE -s "${instance}.png" &> "${instance}.results" &
done

for job in `jobs -p`
do
echo "Waiting for job $job to finish"
    wait $job || let "FAIL+=1"
done
echo $FAIL