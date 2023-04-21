import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import subprocess
import post
import counter
import pandas as pd

if os.path.isdir('..\\flag\\') != True:
    os.system("mkdir {}".format('..\\flag\\'))
    print("create folder: {}".format('..\\flag\\')) 

class MyHandler(FileSystemEventHandler):
    def __init__(self, folder_to_monitor, executed_files):
        self.folder_to_monitor = folder_to_monitor
        self.executed_files = executed_files

    def on_created(self, event):
        file_path = event.src_path
        file_name = os.path.basename(file_path)
        
        if file_name not in self.executed_files and os.path.isfile(file_path):
            print(f"新檔案已創建: {file_name}")
            self.perform_specific_operation(file_path)
            self.executed_files.add(file_name)

    def perform_specific_operation(self, file_path):
        
        print(f"對 {file_path} 進行特定運算...")
        
        input_path = file_path
        file = file_path.split('\\')[-1]
        output_path = '..\\output\\'+file
        id = file.split('.')[0]
        
        student = post.Post_dection(input_path)
        post_df = student.dection()

        a = counter.Body_point(post_df)
        for i in range(2):
            a.get_amplitude()
            a.get_wavelength()
            
        ans = a.jump_rope_count()  
        print('\nid :{} time :{}\n'.format(id,ans))
        
        df = pd.read_json('..\\Backend\\contestants.json')
        df.loc[df['ID'] == id, '成績'] = ans
        df.to_json('..\\Backend\\contestants.json',orient='records')
        
        flag = a.make_flag()
        df = pd.DataFrame(flag)
        df.to_csv('..\\flag\\'+id+'.csv',index=False)
        
        #student.make_output_vidoe(output_path,flag)

def monitor_folder(folder_to_monitor):
    executed_files = set()
    event_handler = MyHandler(folder_to_monitor, executed_files)
    observer = Observer()
    observer.schedule(event_handler, folder_to_monitor, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    folder_to_monitor = "..\\input\\"  # 更改為要監控的資料夾路徑
    monitor_folder(folder_to_monitor)
