import matplotlib.pyplot as plt
import numpy as np
from c0_READ_PATH_FILE import read_file_name

def Plotting(text_infile="Loss_epoch.txt"):
    data = open(text_infile,'r')
    l_epoch=[]; l_val_loss=[]; l_val_error=[]; l_train_loss=[]; l_train_error=[]
    for line in data:
        if "Epoch" in line: continue
        Epoch, Val_loss, Val_error, Train_loss, Train_error = line.split()
        l_epoch.append(int(Epoch)); l_val_loss.append(float(Val_loss))
        l_val_error.append(float(Val_error)); l_train_loss.append(float(Train_loss))
        l_train_error.append(float(Train_error))

    fig = plt.figure()
    ax_loss = fig.add_subplot(111)
    #ax_acc.plot(range(1,len(l_epoch)+1), l_epoch, label='Epoch', color='blue')
    ax_loss.set_xlabel('Epoch')
    ax_loss.plot(range(1,len(l_epoch)+1), l_val_loss, label='Validation Loss', color='blue')    
    ax_loss.plot(np.nan, 'black', label="Validation Error/Accuracy")
    ax_loss.plot(range(1,len(l_epoch)+1), l_train_loss, label='Train Loss', color='red')
    ax_loss.plot(np.nan, 'green', label="Train Error/Accuracy")
    ax_loss.set_ylabel('Loss-value Scale', color='red')
    ax_err = ax_loss.twinx()
    ax_err.plot(range(1,len(l_epoch)+1), l_val_error, label='Validation Error', color='black')
    ax_err.plot(range(1,len(l_epoch)+1), l_train_error, label='Train Error', color='green')
    ax_err.set_ylabel('Error/Accuracy Scale', color='blue')

    ax_loss.legend(loc=0)
    SaveDir = read_file_name(text_infile)[3] + "/Plot_Loss_epoch.pdf"
    plt.savefig(SaveDir)
    #plt.show()
    
def main():
    infile = "./Loss_epoch.txt"
    Plotting(text_infile=infile)


if __name__=="__main__":
    main()

