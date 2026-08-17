import sys
import os
import time
import schedule
import shutil
import hashlib
import zipfile

def Make_zip(folder):
    timestamp=time.strftime("%Y-%m-%d_%H-%M-%S")
    zip_name=folder + "_"+timestamp +".zip"

    #open the zip file

    zobj=zipfile.ZipFile(zip_name,'w',zipfile.ZIP_DEFLATED) #Make zip 

    for root,dirs,files in os.walk(folder):
        for file in files:
            full_path=os.path.join(root,file)
            relative=os.path.relpath(full_path,folder)

            zobj.write(full_path,relative)

    zobj.close()

    return zip_name

    
def Calculate_hash(path):
    hobj=hashlib.md5()
    fobj=open(path,"rb")

    while True:
        data=fobj.read(1024)
        if not data:
            break
        else:
            hobj.update(data)

    fobj.close()

    return hobj.hexdigest()

def BackupFiles(Source,Destination):
    copied_files=[]
    print("Creating the Backup folder for Back Process")
    

    os.makedirs(Destination,exist_ok=True)

    for root,dirs,files in os.walk(Source):
        for file in files:
            src_path=os.path.join(root,file)

            relative=os.path.relpath(src_path,Source)
            dest_path=os.path.join(Destination,relative)

            os.makedirs(os.path.dirname(dest_path),exist_ok=True) #makedir makes nested folder in Destination

            #copy the if its new
            if(not os.path.exists(dest_path) or (Calculate_hash(src_path) != Calculate_hash (dest_path))):
                shutil.copy2(src_path,dest_path) #copy2 -:copy one file and its metadata to destination folder
                copied_files.append(relative)

    return copied_files


def MarvellousDataShieldStart(Source="Data"):

    Border = "-"*50
    print(Border)
    BackupName="MarvellousBackup"

   
    print(Border)
    print("BackUp Process started Successfully at ",time.ctime())
    print(Border)

    files=BackupFiles(Source,BackupName)
   
    zip_file=Make_zip(BackupName)

    print(Border)
    print("Backup completed successfully ")
    print("Files copied :",len(files))
    print("Zip Files get created :",zip_file)
    print(Border)



def main():

    Border = "-"*50
    print(Border)
    print("------- Marvellous Data Shield System --------")
    print(Border)

    if(len(sys.argv) == 2):
        if(sys.argv[1] == "--h" or sys.argv[1] == "--H"):
            print("This scipt is used to : ")
            print("1 : Takes Auto Backup at given time ")
            print("2 : Backup only new and Updated Files ")
            print("3 : Create an Archive of the Backup  Periodically ")


        elif(sys.argv[1] == "--u" or sys.argv[1] == "--U"):
            print("Use the automation script as")
            print("ScriptName.py TimeInterval SourceDirectory")
            print("TimeInterval : The time in minutes for periodic scheduling")
            print("Source Directory : Name of directory to backed up")


        else:
            print("Unable to proceed as there is no such option")
            print("Please use --h or --u to get more details")
    
    # python Demo.py 5 Data
    elif(len(sys.argv) == 3):
        print("Inside projects logic")
        print("Time interval : ",sys.argv[1])
        print("Directory name : ",sys.argv[2])

        

        # Apply the schedular
        schedule.every(int(sys.argv[1])).minutes.do(MarvellousDataShieldStart, sys.argv[2])
        
        print(Border)
        print("Data Shield System started succesfully")
        print("Time interval in minutes: ",sys.argv[1])
        print("Press Ctrl + C to stop the execution")
        print(Border)

        # Wait till abort
        while True:
            schedule.run_pending()
            time.sleep(1)

    else:
        print("Invalid number of command line arguments")
        print("Unable to proceed as there is no such option")
        print("Please use --h or --u to get more details") 

    print(Border)
    print("--------- Thank you for using our script ---------")
    print(Border)
    
if __name__ == "__main__":
    main()