import face_recognition
import numpy as np
import os
import my_project.Database.BaseManager as dm 
 
class handler:

    
    def __init__(self):
        """
        Initialize instance variables
        """
        self.known_faces=[]
        self.labels=[]
        self.bd=dm.Base()
        self.path = os.path.dirname(os.path.realpath(__name__))  #gives me the apsolute path name of current file 
        self.path_uploads = os.path.join(self.path,"my_project", "Web_Server", "uploads")
        self.path_dataset = os.path.join(self.path,"my_project","Live_Recognizer","DataSet" )


    def add(self,direct,name): 
        """
        Adds the features of a face in a list, we can use them to compare later
        """
        face_image=face_recognition.load_image_file(os.path.join(self.path,"my_project","Live_Recognizer", "DataSet", direct,name))
        face_image_features=face_recognition.face_encodings(face_image)[0]
        if(len(face_image_features)!=128):
            print("no face detected")
        else:
            self.known_faces.append(face_image_features)
            self.labels.append(direct)


    def compare(self,image):
        """
        Compare face encodings with data set faces.
        """
        name=''
        names = []
        frame = face_recognition.load_image_file(os.path.join(self.path_uploads,image))
        face_locations = face_recognition.face_locations(frame)   
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        j = 0
        for  face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_faces,face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(self.known_faces,face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.labels[best_match_index]
                self.bd.connect()
                print("Updating "+image)
                self.bd.update(image[:-4]+"_" +str(j)+".jpg",name)
                self.bd.close()
                j +=1
            else :
                j+=1
            names.append(name)
        return(names,frame)

    def scanFaces (self) :
        """
        Scan for new images in upload folder
        """
        for root,dir,files in os.walk(self.path_dataset):            
            if os.path.basename(root) not in self.labels :
                for f in files :
                    if f.endswith(".jpg") :
                        self.add(os.path.basename(root),f)
        print("List",self.labels)





         

