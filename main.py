import subprocess
import datetime
import os
from config import *


#Создать новый бэкап
def create_backup(folder_path, backup_path):

    #Отделяем название папки и путь до родительской папки
    folder_name = folder_path.split('/')[-1]
    parent_folder = '/'.join(folder_path.split('/')[:-1])+'/'

    # формируем имя архива - название папки + текущая дата
    backup_name = '{} {}.tar.gz'.format(folder_name, datetime.datetime.now().date()).replace(' ', '_').replace('-', '_')
    print(backup_name)


    #создаем архив
    subprocess.run(['tar', '-czf', backup_name, '-C', parent_folder, folder_name])

    #перемещаем бэкап в папку с бэкапами
    subprocess.run(['mv', parent_folder+backup_name, backup_path])

    print('Бэкап {} создан'.format(backup_name))



#Удалить старые бэкапы
def delete_old(backup_path, time_limit):

    #Дата, до которой хранятся бэкапы
    limit_date = datetime.datetime.now() - datetime.timedelta(days=time_limit)

    #Проверяем возраст каждого бэкапа в папке с бэкапами и удаляем все, что страше заданного лимита
    for filename in os.listdir(backup_path):
        backup = backup_path+filename
        backup_age = (datetime.datetime.now() - datetime.datetime.fromtimestamp(os.stat(backup).st_atime)).days

        if backup_age >= time_limit:
            os.remove(backup)
            print('Бэкап {} удален'.format(filename))
        else:
            print('Ни один бэкап не удален')



if __name__ == '__main__':
    delete_old(backup_path, time_limit)
    create_backup(folder_path, backup_path)