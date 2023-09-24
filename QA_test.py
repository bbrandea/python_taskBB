import os
import shutil
import logging
import schedule
import time

#create log file
log_file = 'Sync_history.txt'
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

source_folder = r'\private\path\source'
replica_folder = r'\private\path\replica'

#step 1: one-way synchronization:
def synchronize_folders():
    global last_sync_time
    
    try:
        #clear replica folder
        for root, dirs, files in os.walk(replica_folder):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                logging.info(f'File removed: {file_path}')
                print(f'File removed: {file_path}')

        #copy files from source to replica
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                source_file_path = os.path.join(root, file)
                replica_file_path = os.path.join(replica_folder, os.path.relpath(root, source_folder), file)

                #get the file creation time
                file_creation_time = os.path.getctime(source_file_path)
                #check if the file is newly created
                is_new_file = file_creation_time > last_sync_time if last_sync_time else True

                #log and print info about new and copied files
                if is_new_file:
                    shutil.copy2(source_file_path, replica_file_path)
                    logging.info(f'Newly created file: {replica_file_path} (Timestamp: {time.ctime(file_creation_time)})')
                    print(f'Newly created file: {replica_file_path} (Timestamp: {time.ctime(file_creation_time)})')

                    #update the last synchronization time
                    last_sync_time = file_creation_time
                else:
                    shutil.copy2(source_file_path, replica_file_path)
                    logging.info(f'File copied: {source_file_path} -> {replica_file_path}')
                    print(f'File copied: {source_file_path} -> {replica_file_path}')

        #task status update
        logging.info('Source folder synchronized to replica folder.')
        print('Source folder synchronized to replica folder.')

    except Exception as e:
        #mention errors if it's the case
        logging.error(f'Error during synchronization: {str(e)}')
        print(f'Error during synchronization: {str(e)}')

#step 2: synchronization to be performed periodically (in this case, scheduled at every 24 hours):
schedule.every(24).hours.do(synchronize_folders)
#or, if the synchronization is expected to be performed before business hours, please see the suggestion below:
#schedule.every().monday.at("08:00").do(synchronize_folders)
#schedule.every().tuesday.at("08:00").do(synchronize_folders)
#schedule.every().wednesday.at("08:00").do(synchronize_folders)
#schedule.every().thursday.at("08:00").do(synchronize_folders)
#schedule.every().friday.at("08:00").do(synchronize_folders)

#step 3: print sync info; the log file is created according to the command from lines 8 and 9.
if __name__ == "__main__":
    print('Directories one-way synchronization started.')

    last_sync_time = 0  #'0' is set to copy in order to copy all files

    #perform the sync task
    synchronize_folders()

    try:
        while True:
            #scheduled to run automatically and pause for a second
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        #update console in case of manual interruptions
        print('Exiting.')
