# encoding:utf-8
from ftplib import FTP
import os
import fileinput
import os.path
import PySimpleGUI as sg
import sys

# Add some color
# to the window
sg.theme('SandyBeach')
# Very basic window.
# Return values using
# automatic-numbered keys
layout = [
    [sg.Text('Subida de datos FTP')],
    [sg.Text('Cambiar valores por defecto si se necestia: ')],
    # Change the default values
    [sg.Text('IP', size=(15, 1)), sg.InputText("")],
    [sg.Text('Username', size=(15, 1)), sg.InputText("")],
    [sg.Text('Password', size=(15, 1)), sg.InputText(
        "", password_char='*')],
    [sg.Text('Dir FTP', size=(15, 1)), sg.InputText("/mnt/DATA/uploadFiles")],
    [sg.Text('Dir Local', size=(15, 1)), sg.InputText(
        ""), sg.FolderBrowse("Directorio")],
    [sg.RButton('Enviar'), sg.RButton('Verificar')]
]
window = sg.Window('Subida de Archivos de local a FTP', layout)
event, values = window.read()


# ftp COde
ftp = FTP()
myIp = values[0]
# ip 192.168.25.248
myUsername = values[1]
# myUsername maria
myPassword = values[2]
# myPassword maria4711
myDirFtp = values[3]
#  directorio FTP /mnt/DATA/uploadFiles
myDirlocal = values[4]
# directorio local C:\\Users\\georg\\Escritorio\\localDIr

path = (str(myDirlocal)+"\\list.txt")
try:
    if (event == sg.WIN_CLOSED):
        sys.exit()
    else:
        file_exists = os.path.isfile(path)
        ftp.set_debuglevel(2)
        ftp.connect(myIp, 21)
        ftp.login(myUsername, myPassword)
        ftp.cwd(myDirFtp)

except OSError as error:
    print(error)
    sg.popup("Servidor no esta encendido o fallo en conexión")


def auto_upload():

    def ftp_upload(localfile, remotefile):
        fp = open(localfile, 'rb')
        ftp.storbinary('STOR %s' %
                       os.path.basename(localfile), fp, 1024)
        fp.close()
        print("after upload " + localfile + " to " + remotefile)

    def upload_img(file):
        ftp_upload(str(myDirlocal) + "\\" + file, file)

    lastlist = []

    for line in fileinput.input(str(myDirlocal) + "\\list.txt"):
        lastlist.append(line.rstrip("\n"))

    currentlist = os.listdir(myDirlocal)

    newfiles = list(set(currentlist) - set(lastlist))

    if len(newfiles) == 0 and event == 'Enviar':
        print('Upload confirmation', "No files need to upload")
    else:
        for needupload in newfiles:
            print("Uploading " + myDirlocal + "\\" + needupload)
            upload_img(needupload)
            with open(myDirlocal + "\\list.txt", "a") as myfile:
                myfile.write(needupload + "\n")


while True:
    if (event == sg.WIN_CLOSED):
        sys.exit()

    currentlist = os.listdir(myDirlocal)

    lastlist = []

    for line in fileinput.input(str(myDirlocal) + "\\list.txt"):
        lastlist.append(line.rstrip("\n"))
    newfiles = list(set(currentlist) - set(lastlist))

    if (event == 'Verificar'):
        f = open(myDirlocal + "\\list.txt", "r")
        sg.popup('Elementos subidos anteriormente', f.read())

    elif (event == 'Enviar'):
        if(file_exists):
            auto_upload()
            if(len(newfiles) == 0):
                sg.popup('No hay elementos a subir')
            else:
                sg.popup('Subiendo elementos:', newfiles)
                sg.popup('Elementos subido:', newfiles)
        else:
            file = open(myDirlocal + "\\list.txt", "w")
            auto_upload()
    event, values = window.read()
