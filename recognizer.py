from my_project.Live_Recognizer.HOG_Detector import handler
import time
import threading
from PIL import Image
import os


def realtime_scanner(exit) :
    global my_handler,lock
    while(not exit.is_set()) :
        lock.acquire()
        my_handler.scanFaces()
        lock.release()
        time.sleep(20)

def recognizer(exit) :
    global my_handler,done,executed,lock

    while(not exit.is_set()):
        lock.acquire()
        files = os.listdir(my_handler.path_uploads)
        number_of_files=len(files)
        if(executed!=number_of_files):
            for file_name in files: 
                if(file_name not in done):
                    time.sleep(1) 
                    names,frame=my_handler.compare(files[files.index(file_name)])
                    if("Unknown" in names):
                        im=Image.fromarray(frame)
                        im.save(os.path.join(my_handler.path,"my_project","Web_Server","static","unknown",file_name)) 
                    if(names.count("Unknown")!=len(names)):
                        im=Image.fromarray(frame)
                        im.save(os.path.join(my_handler.path,"my_project","Web_Server","static","knowns",file_name))
                    done.append(file_name)
                
        lock.release()

print("Initialisation...")
my_handler=handler()
my_handler.scanFaces()
done=[]
executed=0

exit = threading.Event()
lock = threading.Lock()

t1= threading.Thread(target=realtime_scanner,args=[exit])
t2 = threading.Thread(target=recognizer,args=[exit])
print("Running...")
t1.start()
t2.start()  

try :
    while(1) :
        pass
except KeyboardInterrupt :
    exit.set()
    print("Over.")