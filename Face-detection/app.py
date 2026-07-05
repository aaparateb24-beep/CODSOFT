import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import cv2
# Load Haar Cascade once
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

if face_cascade.empty():
    raise RuntimeError("Failed to load haarcascade_frontalface_default.xml")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app=ctk.CTk()
app.title("😊 Face Detection System")
app.geometry("1000x700")
image_path=None
detected_image=None

def choose_image():
    global image_path
    image_path=filedialog.askopenfilename(filetypes=[("Images","*.jpg *.jpeg *.png")])
    if not image_path:return
    img=Image.open(image_path); img.thumbnail((320,320))
    cimg=ctk.CTkImage(light_image=img,dark_image=img,size=img.size)
    original_label.configure(image=cimg,text=""); original_label.image=cimg
    status.configure(text="✅ Image Selected")

def detect_faces():
    global detected_image
    if image_path is None:
        status.configure(text="❌ Please select an image first."); return
    image=cv2.imread(image_path)
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    face=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.15,
    minNeighbors=7,
    minSize=(60, 60),
    flags=cv2.CASCADE_SCALE_IMAGE
)
    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
    detected_image=image.copy()
    rgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    img=Image.fromarray(rgb); img.thumbnail((320,320))
    cimg=ctk.CTkImage(light_image=img,dark_image=img,size=img.size)
    detected_label.configure(image=cimg,text=""); detected_label.image=cimg
    status.configure(text=f"😊 Faces Detected : {len(faces)}")

def save_image():
    if detected_image is None:
        status.configure(text="❌ Detect faces first."); return
    p=filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("PNG","*.png"),("JPEG","*.jpg")])
    if p:
        cv2.imwrite(p,detected_image); status.configure(text="✅ Image Saved Successfully")

def webcam():
    face=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
    cap=cv2.VideoCapture(0)
    while True:
        ok,frame=cap.read()
        if not ok: break
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.15,
    minNeighbors=7,
    minSize=(60, 60),
    flags=cv2.CASCADE_SCALE_IMAGE
)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(frame,f"Faces: {len(faces)}",(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        cv2.imshow("Webcam Face Detection (Press Q to Quit)",frame)
        if cv2.waitKey(1)&0xFF==ord("q"): break
    cap.release(); cv2.destroyAllWindows()

ctk.CTkLabel(app,text="😊 Face Detection System",font=("Arial",30,"bold")).pack(pady=15)
ctk.CTkLabel(app,text="CODSOFT Internship Project",font=("Arial",16)).pack()
pf=ctk.CTkFrame(app); pf.pack(pady=20)
original_label=ctk.CTkLabel(pf,text="Original Image",width=320,height=320); original_label.grid(row=0,column=0,padx=25,pady=20)
detected_label=ctk.CTkLabel(pf,text="Detected Image",width=320,height=320); detected_label.grid(row=0,column=1,padx=25,pady=20)
bf=ctk.CTkFrame(app); bf.pack(pady=15)
ctk.CTkButton(bf,text="📂 Select Image",command=choose_image,width=180).grid(row=0,column=0,padx=10)
ctk.CTkButton(bf,text="😊 Detect Faces",command=detect_faces,width=180).grid(row=0,column=1,padx=10)
ctk.CTkButton(bf,text="📷 Webcam",command=webcam,width=180).grid(row=0,column=2,padx=10)
ctk.CTkButton(bf,text="💾 Save Image",command=save_image,width=180).grid(row=0,column=3,padx=10)
status=ctk.CTkLabel(app,text="Select an image to begin.",font=("Arial",16)); status.pack(pady=20)
ctk.CTkLabel(app,text="Developed by Aarya • CodSoft AI Internship").pack(side="bottom",pady=15)
app.mainloop()
