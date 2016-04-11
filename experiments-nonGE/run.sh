#!/bin/bash

# The current working directory
BASE_PWD=`pwd`

# City name {manhattan, venice, sanfrancisco}
CITY=sanfrancisco

# The ONE configuration file (template)
CONFIGURATION_FILE=$CITY-FC-0

# The ONE folder
THE_ONE=../one_1.4.1

# Number of repetitions per individual
NR_REP=10

# Simulation length and no. of honest messages
SIM_LENGTH=18000
TOTAL_MSG=600

# Seeds file
SEEDS_FILE=seeds.txt

# Fitness values to extract
FITNESS=(latency_avg)

# individual txt file generated by uGP
INDIVIDUAL_FILE=$1
# individual base name (without extension)
BASE_NAME=${INDIVIDUAL_FILE/.txt/}
# replace wkt file
INDIVIDUAL_WKT=$BASE_NAME"*.wkt"

echo "Evaluating" $BASE_NAME "..."

# parse the individual generated by uGP3 to create a variable number of attackers
python convertToWKT.py $CITY $INDIVIDUAL_FILE

# manipulate configuration file
python editSettings.py $CITY $CONFIGURATION_FILE".txt" $INDIVIDUAL_FILE $NR_REP $SIM_LENGTH > $SEEDS_FILE

# create the temp folder
TMP_DIR=$BASE_NAME
mkdir -p $TMP_DIR

# move the individual files to the temp dir
mv $INDIVIDUAL_WKT $TMP_DIR
mv $CONFIGURATION_FILE"_"$BASE_NAME".txt" $TMP_DIR
mv $SEEDS_FILE $TMP_DIR

# copy the individual wkt file to the ONE data folder
cp $TMP_DIR/$INDIVIDUAL_WKT $THE_ONE/data

# run the ONE simulation (repeated for each seed value)
cd $THE_ONE
./one.sh -b $NR_REP $BASE_PWD/$TMP_DIR/$CONFIGURATION_FILE"_"$BASE_NAME".txt" 

# remove individual wkt file from the ONE data folder
rm data/$INDIVIDUAL_WKT

# parse the log files and evaluate fitnesses
# obtain the first fitness (the DDR/delivery_prob for honest messages)
# this is the mean across all $NR_REP reports of this type
cd $BASE_PWD
# obtain the first fitness
python parseFitness1.py $TMP_DIR $THE_ONE/reports
#mv $THE_ONE/reports/*Delivered* $TMP_DIR
cat $TMP_DIR/*Delivered* | grep M | wc -l | awk -v TM="$TOTAL_MSG" -v NRR="$NR_REP" '{printf "%f ", 1-($1/TM/NRR)}' > $BASE_NAME".out"
# obtain the second fitness
python parseFitness2.py $TMP_DIR $THE_ONE/reports ${FITNESS[*]} >> $BASE_NAME".out"

# copy individual and fitness file to temp dir
#cp $INDIVIDUAL_FILE $TMP_DIR
echo -n "*** "$BASE_NAME" fitnesses: "
cat $BASE_NAME".out"
cp $BASE_NAME".out" $TMP_DIR

# clean temp files
#rm -rf $TMP_DIR