# DTN-security
Simulation configurations and dataset resulted from some studies on the resilience of delay-tolerant network protocols to standard attacks

Prerequisites
- ugp3 3.3.0_645+	http://ugp3.sourceforge.net
- the one 1.4.1+	https://www.netlab.tkk.fi/tutkimus/dtn/theone/
- python 2.7
- numpy 1.10.4+
- java 1.7+

Install and run
- Copy the wkt files from the maps folder to the folder THE_ONE/data
- Edit the run.sh script: 1) Set THE_ONE folder according to your installation folder. 2) Choose CITY (manhattan, venice, sanfrancisco) and CONFIGURATION_FILE. The latter is The ONE template file, used to choose choose the protocol. To select a protocol, replace its name occurrences in CONFIGURATION_FILE (e.g. in sanfrancisco-E-0.txt replace "Epidemic" with FirstContact"). If The ONE template configuration is renamed (e.g. from sanfrancisco-E-0.txt to sanfrancisco-FC-0.txt) this should also reflect into run.sh (e.g. replace $CITY-E-0 with $CITY-FC-0).
- Run ugp3 from the experiment folder (with/without Group Evolution)

Abbrevations
- E: Epidemic
- FC: FirstContact
- SW: SprayAndWait
- GE: Group Evolution
