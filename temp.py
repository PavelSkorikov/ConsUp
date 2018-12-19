import os
import re
import zipfile
import subprocess
import datetime
import ftp_requests

with open('info.txt', 'w') as f:
    f.write(r"""Программа UpCons+ предназначена для синхронизации файлов баз данных 
в локальной папке на сервере(Консультант+) с ftp сервером предприятия и
последующим их автоматическим обновлением в локальной информационной системе 
Консультант+.
    Нужно поместить папку с программой UpCons+ в директорию VEDA\RECEIVE\.
После этого в файле conf.txt первой строкой прописать путь к папке с базами
на FTP - сервере, в следующих 2-х строках изменить даты в именах файлов all и Veda 
на последние загруженные в базу Консультант+. 
    Запуск программы UpCons+.exe настроить на удобное время в системном планировщике задач.

Программу разработал 
инженер - электроник 
Сохрановского ЛПУМГ
ООО "Газпром трансгаз Волгоград"
Скориков П.Г.
pg.skorikov@vlg.gazprom.ru
тел. (751)-68-2-51""")

# функция добавления записи в log-файл
def log_add(s):
    # запись в переменную текущей даты и времени
    dt = datetime.datetime.now()
    dt_now = str(dt.day) + ' ' + str(dt.month) + ' ' + str(dt.year) + ' ' + str(dt.hour) + ':' + str(dt.minute) + ':' + str(dt.second)
    os.chdir('UpCons+')
    with open('log.txt', 'a') as f:
        f.write('\n' + dt_now + s)
    os.chdir('../')
print('Идет процесс обновления информационных баз Консультант+')
# регулярное выражение для взятия даты из имен файлов типа all и Veda
reg_file = re.compile(r'(.*?\d{2})(\d{4}\d{2}\d{2})')
# считываем из файла путь к ftp и имена последних установленных баз all и Veda
with open('conf.txt') as f:
    fb = f.read().split("\n")
ftp_path = fb[0]
all = fb[1]
veda = fb[2]
os.chdir('../')
print('Закачиваю базы с ftp - сервера...')
log_add(' - старт загрузки файлов с ftp')
while
updproc = subprocess.Popen(['UpCons+\Wget\wget.exe', '-c', ftp_path])
res = updproc.wait()
# если процесс закачки завершился с ошибкой, записываем это в log.txt и выходим из программы
if res != 0:
    os.chdir('UpCons+')
    log_add(' - ошибка при закачивании файлов с ftp - сервера')
    os.exit(1)
