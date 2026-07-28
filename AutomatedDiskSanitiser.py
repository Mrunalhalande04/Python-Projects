import hashlib   # it helps to find md5 checksum
import os
import schedule
import sys
import time
import smtplib
from email.message import EmailMessage


# ---------------------- Mail Sending ----------------------

def send_mail(sender, app_password, receiver, subject, body, attachment_path=None):
    Border = "-" * 50
    print(Border)

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.set_content(body)

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
        msg.add_attachment(
            file_data,
            maintype="application",
            subtype="octet-stream",
            filename=file_name,
        )

    smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp.login(sender, app_password)
    smtp.send_message(msg)
    smtp.quit()

    print("Mail sent successfully to", receiver)
    print(Border)


# ---------------------- Checksum / Duplicate Logic ----------------------

def CalculateChecksum(FileName):        # 4567
    fobj = open(FileName, "rb")
    hobj = hashlib.md5()

    Buffer = fobj.read(1000)
    while (len(Buffer) > 0):
        hobj.update(Buffer)
        Buffer = fobj.read(1000)

    fobj.close()
    return hobj.hexdigest()   # give calculation (CheckSum)


def FindDuplicate(DirectoryName):
    Ret = os.path.exists(DirectoryName)
    if (Ret == False):
        print("There is no such directory")
        return

    Ret = os.path.isdir(DirectoryName)
    if (Ret == False):
        print("It is not a directory")
        return

    Duplicate = {}

    for FolderName, SubFolderName, Filename in os.walk(DirectoryName):
        for fname in Filename:
            fname = os.path.join(FolderName, fname)   # join foldername and filename

            Checksum = CalculateChecksum(fname)

            if Checksum in Duplicate:   # Does this checksum already exist as a key
                Duplicate[Checksum].append(fname)
            else:
                Duplicate[Checksum] = [fname]

    return Duplicate


def DeleteDuplicate(Path, MailConfig=None):

    Border = "-" * 50

    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    FileName = os.path.join(Path, "DeletedFiles_%s.log" % timestamp)

    fobj = open(FileName, "w")

    fobj.write(Border + "\n")
    fobj.write("-----------Automated Disk Sanitiser------------\n")
    fobj.write(Border + "\n")

    MyDict = FindDuplicate(Path)

    Result = list(filter(lambda x: len(x) > 1, MyDict.values()))

    Count = 0
    Cnt = 0

    for value in Result:
        for subvalue in value:
            Count = Count + 1
            if (Count > 1):
                fobj.write(Border + "\n")
                fobj.write("Deleted Files :" + subvalue + "\n")
                os.remove(subvalue)
                Cnt = Cnt + 1
        Count = 0

    fobj.write(Border + "\n")
    fobj.write(Border + "\n")
    fobj.write("Total Deleted Files :" + str(Cnt) + "\n")
    fobj.write("This log file is created at " + timestamp + "\n")
    fobj.write(Border + "\n")
    fobj.write("-------------------End of Application-----------------\n")
    fobj.write(Border + "\n")

    fobj.close()   # important: close before emailing, so all content is flushed to disk

    # ---------------- Send the log file over mail ----------------
    if MailConfig is not None:
        subject = "Disk Sanitiser Log - %s" % timestamp
        body = "Hello,\n\nPlease find attached the duplicate-file-deletion log generated at %s.\n\nTotal files deleted: %d\n\nRegards,\nAutomated Disk Sanitiser" % (timestamp, Cnt)

        try:
            send_mail(
                MailConfig["sender"],
                MailConfig["app_password"],
                MailConfig["receiver"],
                subject,
                body,
                attachment_path=FileName,
            )
        except Exception as e:
            print("Failed to send mail:", e)


def main():

    Border = "-" * 50
    print(Border)
    print("---- Automated Disk Sanitiser -----")
    print(Border)

    # ---------------- Mail configuration ----------------
    # Hardcoded credentials. Replace with your own sender/app_password/receiver.
    MailConfig = {
        "sender": "",
        "app_password": "",
        "receiver": "",
    }

    if not all(MailConfig.values()):
        print("Mail credentials not fully set.")
        print("Log files will still be created, but NOT emailed.")
        MailConfig = None

    if (len(sys.argv) == 2):
        if (sys.argv[1] == "--h" or sys.argv[1] == "--H"):
            print("This script is used to : ")
            print("1 : Create automatic logs")
            print("2 : Executes periodically")
            print("3 : Sends mail with the log")
            print("4 : Deletes the Duplicate Files")
            print("5 : Gives record of Deleted Files")

        elif (sys.argv[1] == "--u" or sys.argv[1] == "--U"):
            print("Use the automation script as")
            print("ScriptName.py TimeInterval DirectoryName")
            print("TimeInterval : The time in minutes for periodic scheduling")
            print("DirectoryName : Name of Directory to be Cleaned")

        else:
            print("Unable to proceed as there is no such option")
            print("Please use --h or --u to get more details")

    # python Demo.py 5 Marvellous
    elif (len(sys.argv) == 3):
        print("Automated Disk Sanitiser")
        print("Time interval : ", sys.argv[1])
        print("Directory name : ", sys.argv[2])
        print("Press Ctrl + C to stop the execution")

        # Apply the scheduler
        schedule.every(int(sys.argv[1])).minutes.do(DeleteDuplicate, sys.argv[2], MailConfig)

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
