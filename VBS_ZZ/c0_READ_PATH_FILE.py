import os

def read_file_name(filename):             # returning [filename, filename.txt, absolute path filename.txt, absolute path]

    if(filename[0] == '/'):                 # 'filename' of absoulte location 
        filename = filename
    elif(filename[0] == '~'):
        filename = filename.replace("~",os.environ['HOME'])
    elif((filename[0]=="C")&(filename[1]==":")):
        filename = filename
    else:
        filename = os.getcwd() + "/" + filename

    loca = len(filename)
    for i in range(1,len(filename)+1):       # find the "/" location
        if(filename[-i] == '/'):
            loca = i-1
            break
    FILENAME = filename.replace(filename[:-loca],"")
    FILE = FILENAME.replace(".txt","")    #filetxt
    filename_NoRoot = filename.replace(filename[len(filename)-loca:len(filename)],"")

    filelist = [FILE, FILENAME, filename, filename_NoRoot]
    return(filelist)


def main():
    NAME = read_file_name("../data_txt/BEIJING_Aqi/carbon_copied_data/n4_temp_mean/Aqi_Beijing_TempM.txt")
    print(NAME)


if __name__=="__main__":
    main()
