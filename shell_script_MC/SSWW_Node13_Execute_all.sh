#!/bin/bash
#TODO Working on Screen ENV
export LOCALDIR=`pwd`
export LC_ALL=en_US.UTF-8
export EXECDIR=/home/junho/MG5_aMC_v2_6_1/madgraph/various
cd ${EXECDIR}

export Splited_LHE_Dir=${LOCALDIR}/TL_split/   #FIXME :: Need to be located on split aiming Directory
#export Splited_LHE_Dir=${LOCALDIR}/TL_split_temp/

#FIXME on /home/junho/MG5_aMC_v2_6_1/madgraph/various/lhe_parser_TTTLLL.py  :: Change file name on python script
python ${EXECDIR}/lhe_parser_TTTLLL.py  # choose if you need LHE parsed

export WholeStoreDP=${Splited_LHE_Dir} #Aiming store splitted LHE directory
export PYTHIA8DATA=/home/junho/MG5_aMC_v2_6_1/HEPTools/pythia8/share/Pythia8/xmldoc
export PATH=/home/junho/MG5_aMC_v2_6_1/HEPTools/MG5aMC_PY8_interface/:/home/junho/MG5_aMC_v2_6_1/HEPTools/pythia8/:$PATH
LD_LIBRARY_PATH=/home/junho/MG5_aMC_v2_6_1/Delphes/:$LD_LIBRARY_PATH
export EXECDIR=/home/junho/MG5_aMC_v2_6_1/Delphes/
cd ${EXECDIR}
export DPLHEconfig=/home/junho/MG5_aMC_v2_6_1/Delphes/self_configLHE.cmnd
export DPbatch=${EXECDIR}DP_selfTest
export PATHNtuple=${EXECDIR}VBS_SS_WW_1.py
export list_files=`ls ${Splited_LHE_Dir}`
for i in ${list_files}
do
  export Write_DPLHEconfig=${Splited_LHE_Dir}$i  # The input lhe absolute path
  export wp=wp_
  export decay=decay_
  export wp_LHEconfig=${wp}$i # The input wp_lhe (only name)
  export wpwm_decay_LHEconfig=$i
  export ABSwpwm_decay_LHEconfig=${Splited_LHE_Dir}$i # The input decay_lhe absolute path
  export OnlyName=`echo $i | sed -e "s/.lhe//g"`
  export Name_DPLHEconfig=`echo $i | sed -e "s/lhe/cmnd/g"`
  export DP_outputName=`echo $i | sed -e "s/.lhe/_DP.root/g"` # The DP.root file 
  export Whole_DP_outputName=${WholeStoreDP}${DP_outputName}  # The absolute path included DP.root file
  export DPbatch_Name=`echo $i | sed -e "s/.lhe/_script.sh/g"`
  export Nohub_name=`echo $i | sed -e "s/.lhe/.file/g"`
  export Whole_DPbatch_Name=${EXECDIR}${DPbatch_Name}
  export Tot_Name_DPLHEconfig=${EXECDIR}${Name_DPLHEconfig} #copy to name of config file
  export PathCopy_Ntuple=${EXECDIR}Ntuple_${OnlyName}.py
  cp ${DPLHEconfig} ${Tot_Name_DPLHEconfig}
  cp ${DPbatch} ${Whole_DPbatch_Name}
  cp ${PATHNtuple} ${PathCopy_Ntuple}
  ex -sc '315i|    infile_test = "'${Whole_DP_outputName}'"' -cx ${PathCopy_Ntuple}

  echo ${i}
  
  ###
  #DECAY
  echo "mv ${Write_DPLHEconfig} /home/junho/MadGraph5_v1_5_14/DECAY/" >> ${Whole_DPbatch_Name}
  echo "cd /home/junho/MadGraph5_v1_5_14/DECAY/"  >> ${Whole_DPbatch_Name}
  echo "printf '1\n${i}\n${wp_LHEconfig}\nw+\n5\n' | ./decay" >> ${Whole_DPbatch_Name}
  echo "rm ${i}" >> ${Whole_DPbatch_Name}
  echo "printf '1\n${wp_LHEconfig}\n${wpwm_decay_LHEconfig}\nw-\n5\n' | ./decay" >> ${Whole_DPbatch_Name}
  echo "rm ${wp_LHEconfig}" >> ${Whole_DPbatch_Name}
  echo "mv ${wpwm_decay_LHEconfig} ${ABSwpwm_decay_LHEconfig}" >> ${Whole_DPbatch_Name}
  echo "cd /home/junho/MG5_aMC_v2_6_1/Delphes/" >> ${Whole_DPbatch_Name}
  ###
  

  echo Beams:LHEF = ${Write_DPLHEconfig} >> ${Tot_Name_DPLHEconfig}
  echo ${EXECDIR}DelphesPythia8 ${EXECDIR}delphes_card_CMS.tcl ${Tot_Name_DPLHEconfig} ${Whole_DP_outputName} >> ${Whole_DPbatch_Name}  #execute DelphesPythia
  
  ###
  #NTUPLE write here 
  export dot=\'
  echo "python ${PathCopy_Ntuple}" >> ${Whole_DPbatch_Name}
  ###
 
  echo 'rm '${Whole_DP_outputName} >> ${Whole_DPbatch_Name}  ## Removing all _DP.root
  echo 'rm '${Tot_Name_DPLHEconfig} >> ${Whole_DPbatch_Name} ## removing all "DP's cmnd"
  echo 'rm '${Whole_DPbatch_Name} >> ${Whole_DPbatch_Name}     ## removing all "DP's script"
  echo 'rm '${PathCopy_Ntuple} >> ${Whole_DPbatch_Name}
  nohup ${Whole_DPbatch_Name} > ${Nohub_name} 2>&1 &

done









