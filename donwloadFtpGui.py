import sys
import ftplib
import os
import time
import errno
import os.path
import PySimpleGUI as sg

layout = [
    [sg.Text('Descarga de datos por FTP')],
    [sg.Text('Cambiar valores por defecto de ser necesario: ')],
    # Change the default values
    [sg.Text('IP', size=(15, 1)), sg.InputText("")],
    [sg.Text('Username', size=(15, 1)), sg.InputText("")],
    [sg.Text('Password', size=(15, 1)), sg.InputText(
        "", password_char='*')],
    [sg.Text('Dir FTP', size=(15, 1)), sg.InputText("")],
    [sg.Text('Dir Local', size=(15, 1)), sg.InputText(
        ""), sg.FolderBrowse("Directorio")],
    [sg.RButton('Descargar')]
]

window = sg.Window('Descarga de archivos por FTP a Local', layout)
event, values = window.read()


# Valores por defecto
server = values[0]
user = values[1]
password = values[2]
source = values[3]
destination = values[4]
interval = 0.05
try:
    if (event == sg.WIN_CLOSED):
        sys.exit()
    else:
        ftp = ftplib.FTP(server)
        ftp.login(user, password)
except OSError as error:
    print(error)
    sg.popup("Servidor no encendido o fallo en conexión")


def downloadFiles(path, destination):

    try:
        ftp.cwd(path)
        os.chdir(destination)
        mkdir_p(destination[0:len(destination)-1])
        print("Created: " + destination[0:len(destination)-1])
    except OSError:
        pass
    except ftplib.error_perm:
        print("Error: could not change to ")
        sys.exit("Ending Application")

    filelist = ftp.nlst()

    for file in filelist:
        time.sleep(interval)
        try:
            ftp.cwd(file + "/")
            downloadFiles(file + "/", destination)
        except ftplib.error_perm:
            os.chdir(destination[0:len(destination)-1])

            try:
                ftp.retrbinary(
                    "RETR " + file, open(os.path.join(destination, file), "wb").write)
                print("Downloaded: " + file)
            except:
                print("Error: File could not be downloaded " + file)
    return


def mkdir_p(path):

    try:
        os.makedirs(path)

    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


while True:
    if (event == 'Descargar'):
        sg.popup('Elementos seran descargados en breve', 'Click en OK :')
        downloadFiles(source, destination)
        if(len(os.listdir(destination)) == 0):
            sg.popup('No hay elementos descargados')
        else:
            sg.popup('Elementos descargados', os.listdir(destination))

    event, values = window.read()
    if (event == sg.WIN_CLOSED or event == 'Cancel'):
        break
