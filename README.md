# DTN-security
Simulation configurations used for studying the resilience of delay-tolerant network (DTN) protocols to standard attacks.

References
- D. Bucur, G. Iacca, M. Gaudesi, G. Squillero, A. Tonda, Optimizing groups of colluding strong attackers in mobile urban communication networks with evolutionary algorithms, Applied Soft Computing, Elsevier, Volume 40, Pages 416-426, March 2016 [bib](http://dblp.uni-trier.de/rec/bibtex/journals/asc/BucurIGST16)
- D. Bucur, G. Iacca, G. Squillero, A. Tonda, Black Holes and Revelations: Using Evolutionary Algorithms to Uncover Vulnerabilities in Disruption-Tolerant Networks, Proc. of EvoApps, LNCS, Springer, Copenaghen, March 2015 [bib](http://dblp.uni-trier.de/rec/bibtex/conf/evoW/BucurIST15)

Prerequisites
- ugp3 3.3.0_645+	http://ugp3.sourceforge.net
- the one 1.4.1+	https://www.netlab.tkk.fi/tutkimus/dtn/theone/
- python 2.7
- numpy 1.10.4+
- java 1.7+

Install and run
- Copy the wkt files from the maps folder to the folder THE_ONE/data
- Edit the run.sh script: 1) Set THE_ONE folder according to your installation folder. 2) Choose CITY (manhattan, venice, sanfrancisco) and CONFIGURATION_FILE. The latter is The ONE template file, used to choose the network protocol. To select a protocol, replace its name occurrences in CONFIGURATION_FILE (e.g. in sanfrancisco-E-0.txt replace "Epidemic" with FirstContact"). If The ONE template configuration is renamed (e.g. from sanfrancisco-E-0.txt to sanfrancisco-FC-0.txt) this should also reflect into run.sh (e.g. replace $CITY-E-0 with $CITY-FC-0).
- Run ugp3 from the experiment folder (with/without Group Evolution)

Abbrevations
- E: Epidemic
- FC: FirstContact
- SW: SprayAndWait
- GE: Group Evolution
