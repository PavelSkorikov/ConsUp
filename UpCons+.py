import os
import re
import zipfile
import subprocess
import datetime

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
    dt_now = str(dt.day)+' '+str(dt.month)+' '+str(dt.year)+' '+str(dt.hour)+':'+str(dt.minute)+':'+str(dt.second)
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
print('Закачиваю базы с ftp - сервера...')
log_add(' - старт загрузки файлов с ftp')
updproc = subprocess.Popen(['UpCons+\Wget\wget.exe', '-c', ftp_path])
updproc.wait()
# если процесс закачки завершился с ошибкой, записываем это в log.txt и выходим из программы
if updproc.wait() != 0:
    log_add(' - ошибка при закачивании файлов с ftp - сервера')
    os._exit(1)
max_all = 0
print('Распаковываю файлы баз...')
log_add(' - распаковка скачанных файлов')
for fl in os.listdir(os.getcwd()):
# выбираем файл Veda в папке, моложе последнего загруженного файла и распаковываем его в директорию на уровень выше
    if fl[:4] == 'Veda':
        if int(reg_file.search(veda).group(2)) < int(reg_file.search(fl).group(2)):
            unzip = zipfile.ZipFile(fl)
            unzip.extractall('../')
            unzip.close()
            veda = fl
# выбираем файлы all моложе последнего загруженного и распаковываем их в текущую директорию
    if fl[:3] == 'all':
        if int(reg_file.search(all).group(2)) < int(reg_file.search(fl).group(2)):
            upzip = zipfile.ZipFile(fl)
            upzip.extractall()
            upzip.close()
            if int(reg_file.search(fl).group(2)) > max_all:
                max_all = int(reg_file.search(fl).group(2))
                all = fl
print('Идет обновление...')
log_add(' - старт обновления')
# запускаем обновление Консультант+
updproc = subprocess.Popen(['../cons.exe', '/adm', '/receive', '/base*', '/sendstt', '/yes'])
updproc.wait()
if updproc.wait() != 0:
    os.chdir('UpCons+')
    log_add(' - ошибка обновления баз')
    os._exit(1)
print('Удаляю ненужные файлы...')
for filename in os.listdir(os.getcwd()):
    if filename.endswith('.txt') or filename.endswith('.ANS') or filename.endswith('.USR') or filename.endswith('.TXT'):
        os.unlink(filename)
log_add(' - обновление прошло успешно')
# записываем в файл conf.txt имена файлов последних загруженных баз
os.chdir('UpCons+')
with open('conf.txt', 'w') as f:
    f.write(ftp_path + '\n' + all + '\n' + veda)












