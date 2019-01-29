#!/bin/bash
##############
export LOCALDIR=/eos/cms/store/user/junho/ttbar/batch1/   #FIXME #FIXME #FIXME
export LC_ALL=en_US.UTF-8
export EXECDIR=/afs/cern.ch/user/j/junho/work/MyAnalysis_IPHC2/CMSSW_8_0_23/src/MG5_aMC_v2_5_5/madgraph/various
cd ${EXECDIR}

export Splited_LHE_Dir=${LOCALDIR}   #Need to be located on split aiming Directory 

#FIXME on /afs/cern.ch/user/j/junho/work/MyAnalysis_IPHC2/CMSSW_8_0_23/src/MG5_aMC_v2_5_5/madgraph/various/lhe_parser_TTTLLL_10.py  :: Change file name on python script
#python ${EXECDIR}/lhe_parser_TTTLLL_10.py  # choose if you need LHE parsed

export WholeStoreDP=${Splited_LHE_Dir} #Aiming store splitted LHE directory
export PYTHIA8DATA=/afs/cern.ch/user/j/junho/work/MyAnalysis_IPHC2/CMSSW_8_0_23/src/MG5_aMC_v2_5_5/HEPTools/pythia8/share/Pythia8/xmldoc
export PATH=/afs/cern.ch/user/j/junho/work/MyAnalysis_IPHC2/CMSSW_8_0_23/src/MG5_aMC_v2_5_5/HEPTools/MG5aMC_PY8_interface/:/afs/cern.ch/user/j/junho/work/MyAnalysis_IPHC2/CMSSW_8_0_23/src/MG5_aMC_v2_5_5/HEPTools/pythia8/:$PATH
LD_LIBRARY_PATH=/afs/cern.ch/user/j/junho/work/MyAnalysis_IPHC2/CMSSW_8_0_23/src/MG5_aMC_v2_5_5/Delphes/:$LD_LIBRARY_PATH
export EXECDIR=/afs/cern.ch/user/j/junho/work/MyAnalysis_IPHC2/CMSSW_8_0_23/src/MG5_aMC_v2_5_5/Delphes/
cd ${EXECDIR}
export DPLHEconfig=/afs/cern.ch/user/j/junho/work/MyAnalysis_IPHC2/CMSSW_8_0_23/src/MG5_aMC_v2_5_5/Delphes/configLHE_ttbar.cmnd
export DPbatch=${EXECDIR}DP_selfTest
export PATHNtuple=${EXECDIR}VBS_SS_WW_ttbar_test.py
export list_files=`ls ${Splited_LHE_Dir}`
for i in ${list_files}
do
  export Write_DPLHEconfig=${Splited_LHE_Dir}$i/phamom.lhe  # The input lhe absolute path
  echo ${Write_DPLHEconfig}
  gunzip ${Write_DPLHEconfig}.gz
  export wp=wp_
  export decay=decay_
  export wp_LHEconfig=${wp}$i # The input wp_lhe (only name)
  export wpwm_decay_LHEconfig=$i
  export ABSwpwm_decay_LHEconfig=${Splited_LHE_Dir}$i # The input decay_lhe absolute path
  #export OnlyName=`echo $i | sed -e "s/.lhe//g" #former FIXME`
  export OnlyName=`echo $i`
  #export Name_DPLHEconfig=`echo $i | sed -e "s/lhe/cmnd/g"` #former FIXME
  export Name_DPLHEconfig=`echo $i.cmnd`
  #export DP_outputName=`echo $i | sed -e "s/.lhe/_DP.root/g"` # The DP.root file #former FIXME 
  export DP_outputName=${i}_DP.root
  export Whole_DP_outputName=${WholeStoreDP}${DP_outputName}  # The absolute path included DP.root file
  #export DPbatch_Name=`echo $i | sed -e "s/.lhe/_script.sh/g"` #former FIXME
  export DPbatch_Name=${i}_script.sh
  #export Nohub_name=`echo $i | sed -e "s/.lhe/.file/g"` #former FIXME
  export Nohub_name=`echo $i.file`
  export Whole_DPbatch_Name=${EXECDIR}${DPbatch_Name}
  export Tot_Name_DPLHEconfig=${EXECDIR}${Name_DPLHEconfig} #copy to name of config file
  export PathCopy_Ntuple=${EXECDIR}Ntuple_${OnlyName}.py
  cp ${DPLHEconfig} ${Tot_Name_DPLHEconfig}
  cp ${DPbatch} ${Whole_DPbatch_Name}
  cp ${PATHNtuple} ${PathCopy_Ntuple}
  ex -sc '325i|    infile_test = "'${Whole_DP_outputName}'"' -cx ${PathCopy_Ntuple}

  echo ${i}
 
  ###
  ##DECAY
  #echo "mv ${Write_DPLHEconfig} /afs/cern.ch/user/j/junho/work/MyAnalysis_IPHC2/CMSSW_8_0_23/src/MadGraph5_v1_5_14/DECAY/" >> ${Whole_DPbatch_Name}
  #echo "cd /afs/cern.ch/user/j/junho/work/MyAnalysis_IPHC2/CMSSW_8_0_23/src/MadGraph5_v1_5_14/DECAY/"  >> ${Whole_DPbatch_Name}
  #echo "printf '1\n${i}\n${wp_LHEconfig}\nw+\n5\n' | ./decay" >> ${Whole_DPbatch_Name}
  #echo "rm ${i}" >> ${Whole_DPbatch_Name}
  #echo "printf '1\n${wp_LHEconfig}\n${wpwm_decay_LHEconfig}\nw-\n5\n' | ./decay" >> ${Whole_DPbatch_Name}
  #echo "rm ${wp_LHEconfig}" >> ${Whole_DPbatch_Name}
  #echo "mv ${wpwm_decay_LHEconfig} ${ABSwpwm_decay_LHEconfig}" >> ${Whole_DPbatch_Name}
  #echo "cd /afs/cern.ch/user/j/junho/work/MyAnalysis_IPHC2/CMSSW_8_0_23/src/MG5_aMC_v2_5_5/Delphes/" >> ${Whole_DPbatch_Name}
  ###

  echo Beams:LHEF = ${Write_DPLHEconfig} >> ${Tot_Name_DPLHEconfig}
  echo ${EXECDIR}DelphesPythia8 ${EXECDIR}delphes_card_CMS.tcl ${Tot_Name_DPLHEconfig} ${Whole_DP_outputName} >> ${Whole_DPbatch_Name}  #execute DelphesPythia
  echo "cd /afs/cern.ch/user/j/junho/work/MyAnalysis_IPHC2/CMSSW_8_0_23/src/MG5_aMC_v2_5_5/Delphes" >> ${Whole_DPbatch_Name}  
  ###
  #NTUPLE write here 
  export dot=\'
  echo 'eval `scramv1 runtime -sh`' >> ${Whole_DPbatch_Name}  # equivalent to cmsenv
  echo "python ${PathCopy_Ntuple}" >> ${Whole_DPbatch_Name}
  ###
 
  echo 'rm '${Whole_DP_outputName} >> ${Whole_DPbatch_Name}  ## Removing all _DP.root
  echo 'rm '${Tot_Name_DPLHEconfig} >> ${Whole_DPbatch_Name} ## removing all "DP's cmnd"
  echo 'rm '${Whole_DPbatch_Name} >> ${Whole_DPbatch_Name}     ## removing all "DP's script (~.sh)"
  echo 'rm '${PathCopy_Ntuple} >> ${Whole_DPbatch_Name}   ## remove Ntuple
  echo '#rm '${Splited_LHE_Dir}${i}/phamom.lhe >> ${Whole_DPbatch_Name}  ## remove origin LHE
  ###nohup ${Whole_DPbatch_Name} > ${Nohub_name} 2>&1 &
  bsub -q 1nd ${Whole_DPbatch_Name}

done









