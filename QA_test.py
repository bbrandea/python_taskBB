import os
import shutil
import logging
import schedule
import time

log_file = 'Sync_history.txt'
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

source_folder = r'\private\path\source'
replica_folder = r'\private\path\replica'

#step 1: one-way synchronization:
def synchronize_folders():
    try:
        for root, dirs, files in os.walk(replica_folder):
            for file in files:
                os.remove(os.path.join(root, file))
                logging.info(f'File removed: {os.path.join(root, file)}')

        for root, dirs, files in os.walk(source_folder):
            for file in files:
                shutil.copy2(os.path.join(root, file), os.path.join(replica_folder, os.path.relpath(root, source_folder), file))
                logging.info(f'File copied: {os.path.join(root, file)} -> {os.path.join(replica_folder, os.path.relpath(root, source_folder), file)}')

        logging.info('Source folder synchronized to replica folder.')

    except Exception as e:
        logging.error(f'Error during synchronization: {str(e)}')

#step 2: synchronization to be performed periodically (in this case, scheduled at every 24 hours):
schedule.every(24).hours.do(synchronize_folders)
#or, if the synchronization is expected to be performed before business hours, please see the suggestion below:
#schedule.every().monday.at("08:00").do(synchronize_folders)
#schedule.every().tuesday.at("08:00").do(synchronize_folders)
#schedule.every().wednesday.at("08:00").do(synchronize_folders)
#schedule.every().thursday.at("08:00").do(synchronize_folders)
#schedule.every().friday.at("08:00").do(synchronize_folders)

#step 3: print sync info; the log file is created according to the queries from lines 7 and 8.
if __name__ == "__main__":
    print('Directories one-way synchronization started.')
    synchronize_folders()

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print('Exiting.')
