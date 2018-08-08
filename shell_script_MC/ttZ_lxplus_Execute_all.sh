#!/bin/bash

export LOCALDIR=`pwd`
export EXECDIR=/afs/cern.ch/user/j/junho/work/MyAnalysis_IPHC2/CMSSW_8_0_23/src/MG5_aMC_v2_5_5/madgraph/various
export LC_ALL=en_US.UTF-8
#export PATH=/afs/cern.ch/user/j/junho/work/MyAnalysis_IPHC2/CMSSW_8_0_23/src/MG5_aMC_v2_5_5/madgraph/various
export PYTHONPATH=/cvmfs/cms.cern.ch/crab3/slc6_amd64_gcc493/cms/crabclient/3.3.1805.patch1/lib/python2.7/site-packages:/cvmfs/cms.cern.ch/crab3/slc6_amd64_gcc493/cms/dbs3-client/3.5.1//lib/python2.7/site-packages:/cvmfs/cms.cern.ch/crab3/slc6_amd64_gcc493/cms/dbs3-pycurl-client/3.5.1/lib/python2.7/site-packages:$PYTHONPATH
cd ${EXECDIR}

#FIXME on Splited_LHE_Dir correspond with output from lhe_parser.py
export Splited_LHE_Dir=/eos/cms/store/user/junho/To_lxplus_ttZ/1M/batch10/split/  #FIXME keep 'split/'

#FIXME on /afs/cern.ch/user/j/junho/work/MyAnalysis_IPHC2/CMSSW_8_0_23/src/MG5_aMC_v2_5_5/madgraph/various/lhe_parser.py
#python ${EXECDIR}/lhe_parser.py  # choose if you need LHE parsed

#FIXME
#export WholeStoreDP=/tmp/junho/
#export WholeStoreDP=/eos/cms/store/user/junho/ttz_test/split/
export WholeStoreDP=${Splited_LHE_Dir}

export PYTHIA8DATA=/afs/cern.ch/user/j/junho/work/MyAnalysis_IPHC2/CMSSW_8_0_23/src/MG5_aMC_v2_5_5/HEPTools/pythia8/share/Pythia8/xmldoc
export PATH=/afs/cern.ch/user/j/junho/work/MyAnalysis_IPHC2/CMSSW_8_0_23/src/MG5_aMC_v2_5_5/HEPTools/MG5aMC_PY8_interface/:/afs/cern.ch/user/j/junho/work/MyAnalysis_IPHC2/CMSSW_8_0_23/src/MG5_aMC_v2_5_5/HEPTools/pythia8/:$PATH
LD_LIBRARY_PATH=/afs/cern.ch/user/j/junho/work/MyAnalysis_IPHC2/CMSSW_8_0_23/src/MG5_aMC_v2_5_5/Delphes/:$LD_LIBRARY_PATH
export EXECDIR=/afs/cern.ch/user/j/junho/work/MyAnalysis_IPHC2/CMSSW_8_0_23/src/MG5_aMC_v2_5_5/Delphes/
cd ${EXECDIR}
export DPLHEconfig=/afs/cern.ch/user/j/junho/work/MyAnalysis_IPHC2/CMSSW_8_0_23/src/MG5_aMC_v2_5_5/Delphes/self_configLHE.cmnd
export DPbatch=${EXECDIR}DP_selfTest
export list_files=`ls ${Splited_LHE_Dir}`
for i in ${list_files}
do   #  Make DelpherPythia LHE config Files
  export Write_DPLHEconfig=${Splited_LHE_Dir}$i  # The input lhe absolute path
  export Name_DPLHEconfig=`echo $i | sed -e "s/lhe/cmnd/g"`
  export DP_outputName=`echo $i | sed -e "s/.lhe/_DP.root/g"` # The DP.root file 
  export Whole_DP_outputName=${WholeStoreDP}${DP_outputName}  # The absolute path included DP.root file 
  export DPbatch_Name=`echo $i | sed -e "s/.lhe/_script/g"`
  export Ntuple_run_name=`echo $i | sed -e "s/.lhe/_run.C/g"` #FIXME
  export Ntuple_TestEx_name=`echo $i | sed -e "s/.lhe/_TestEx.C/g"` #FIXME
  export Ntuple_outfilename=`echo $i | sed -e "s/.lhe/_Ntuple.root/g"` #FIXME
  #echo ${Ntuple_run_name}
  #echo ${Ntuple_TestEx_name}
  #echo ${Whole_DP_outputName}
  #echo ${Ntuple_outfilename}
  export Whole_DPbatch_Name=${EXECDIR}${DPbatch_Name}
  export Tot_Name_DPLHEconfig=${EXECDIR}${Name_DPLHEconfig} #copy to name of config file
  cp ${DPLHEconfig} ${Tot_Name_DPLHEconfig}
  cp ${DPbatch} ${Whole_DPbatch_Name}

  echo Beams:LHEF = ${Write_DPLHEconfig} >> ${Tot_Name_DPLHEconfig}
  echo export LSB_JOB_REPORT_MAIL=N >> ${Whole_DPbatch_Name}
  echo ${EXECDIR}DelphesPythia8 ${EXECDIR}delphes_card_CMS.tcl ${Tot_Name_DPLHEconfig} ${Whole_DP_outputName} >> ${Whole_DPbatch_Name}
  echo ls >> ${Whole_DPbatch_Name}
  echo echo TESTTESTTEST >> ${Whole_DPbatch_Name}
  #echo cp ${Whole_DP_outputName} ${Splited_LHE_Dir} >> ${Whole_DPbatch_Name}
  #echo ${Whole_DPbatch_Name}

  echo export EXEDIR=/afs/cern.ch/user/j/junho/work/MyAnalysis_IPHC2/CMSSW_8_0_23/src/New_IPHCNtuple/IPHCNtuple/MEM/DelphesAnalyzer/ >> ${Whole_DPbatch_Name}
  echo LD_LIBRARY_PATH=/afs/cern.ch/user/j/junho/work/MyAnalysis_IPHC2/CMSSW_8_0_23/src/MG5_aMC_v2_5_5/Delphes/:$LD_LIBRARY_PATH >> ${Whole_DPbatch_Name}  ## export ?
  echo export LC_ALL=en_US.UTF-8 >> ${Whole_DPbatch_Name}
  echo cd '${EXEDIR}' >> ${Whole_DPbatch_Name}
  echo 'eval `scramv1 runtime -sh`' >> ${Whole_DPbatch_Name}  # equivalent to cmsenv
  ## cp, insert, run
  echo 'export Ntuple_run_name='${Ntuple_run_name} >> ${Whole_DPbatch_Name}
  echo 'export Ntuple_TestEx_name='${Ntuple_TestEx_name} >>${Whole_DPbatch_Name}
  echo 'export Ntuple_outfilename='${Ntuple_outfilename} >>${Whole_DPbatch_Name}
  echo 'export Splited_LHE_Dir='${Splited_LHE_Dir} >>${Whole_DPbatch_Name}
  echo cp '${EXEDIR}copy_run.C ${EXEDIR}${Ntuple_run_name}' >> ${Whole_DPbatch_Name} 
  echo cp '${EXEDIR}copy_TestExRootAnalysis.C ${EXEDIR}${Ntuple_TestEx_name}' >> ${Whole_DPbatch_Name}
  export dot=\'
  echo ex -sc ${dot}'5i|  gROOT->ProcessLine(".L '${Ntuple_TestEx_name}'+");'${dot} -cx ${Ntuple_run_name} >> ${Whole_DPbatch_Name}
  echo ex -sc ${dot}'48i|  chain.Add("'${Whole_DP_outputName}'");'${dot} -cx ${Ntuple_TestEx_name} >> ${Whole_DPbatch_Name}
  echo ex -sc ${dot}'104i|  TFile* fOutput = new TFile("'${Splited_LHE_Dir}${Ntuple_outfilename}'","RECREATE");'${dot} -cx ${Ntuple_TestEx_name} >> ${Whole_DPbatch_Name}
  echo 'rm '${Splited_LHE_Dir}${i} >> ${Whole_DPbatch_Name}
  echo 'root -l -b -q ' ${Ntuple_run_name} >> ${Whole_DPbatch_Name}
  echo 'rm '${Whole_DP_outputName} >> ${Whole_DPbatch_Name}
  echo 'mv '${Splited_LHE_Dir}${Ntuple_outfilename} ${Splited_LHE_Dir}.. >> ${Whole_DPbatch_Name} 
  echo rm '${EXEDIR}${Ntuple_run_name}' >> ${Whole_DPbatch_Name}
  echo rm '${EXEDIR}${Ntuple_TestEx_name}' >> ${Whole_DPbatch_Name}
  echo 'rm '${EXECDIR}${Name_DPLHEconfig} >> ${Whole_DPbatch_Name}
  echo 'rm '${EXECDIR}${DPbatch_Name} >> ${Whole_DPbatch_Name}

  bsub -q 1nw ${Whole_DPbatch_Name}
done



