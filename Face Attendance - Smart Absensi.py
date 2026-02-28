import cv2, os, numpy as np
import tkinter as tk
from PIL import ImageTk, Image
from datetime import datetime

def selesai1():
    instructions.config(text="Rekam Data Telah Selesai!")
def selesai2():
    instructions.config(text="Training Wajah Telah Selesai!")
def selesai3():
    instructions.config(text="Absensi Telah Dilakukan")

def rekamDataWajah():
    wajahDir = 'datawajah' 
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)
    faceDetector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eyeDetector = cv2.CascadeClassifier('haarcascade_eye.xml')
    faceID = entry2.get()
    nama = entry1.get()
    nim = entry2.get()
    kelas = entry3.get()
    ambilData = 1
    while True:
        retV, frame = cam.read()
        abuabu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceDetector.detectMultiScale(abuabu, 1.3, 5)
        for (x, y, w, h) in faces:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            namaFile = str(nim) +'_'+str(nama) + '_' + str(kelas) +'_'+ str(ambilData) +'.jpg'
            cv2.imwrite(wajahDir + '/' + namaFile, frame)
            ambilData += 1
            roiabuabu = abuabu[y:y + h, x:x + w]
            roiwarna = frame[y:y + h, x:x + w]
            eyes = eyeDetector.detectMultiScale(roiabuabu)
            for (xe, ye, we, he) in eyes:
                cv2.rectangle(roiwarna, (xe, ye), (xe + we, ye + he), (0, 255, 255), 1)
        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Stop on 'q' key
            break
        elif ambilData > 1:
            break
    selesai1()
    cam.release()
    cv2.destroyAllWindows()

def trainingWajah():
    wajahDir = 'datawajah'
    latihDir = 'latihwajah'

    def getImageLabel(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faceSamples = []
        faceIDs = []
        for imagePath in imagePaths:
            PILimg = Image.open(imagePath).convert('L')
            imgNum = np.array(PILimg, 'uint8')
            faceID = int(os.path.split(imagePath)[-1].split('_')[0])
            faces = faceDetector.detectMultiScale(imgNum)
            for (x, y, w, h) in faces:
                faceSamples.append(imgNum[y:y + h, x:x + w])
                faceIDs.append(faceID)
            return faceSamples, faceIDs

    faceRecognizer = cv2.face.LBPHFaceRecognizer_create()
    faceDetector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces, IDs = getImageLabel(wajahDir)
    faceRecognizer.train(faces, np.array(IDs))
    faceRecognizer.write(latihDir + '/training.xml')
    selesai2()

def markAttendance(name):
    with open("Attendance.csv",'r+') as f:
        namesDatalist = f.readlines()
        namelist = []
        yournim = entry2.get()
        yourclass = entry3.get()
        for line in namesDatalist:
            entry = line.split(',')
            namelist.append(entry[0])
        if name not in namelist:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{yourclass},{yournim},{dtString}')

def absensiWajah():
    wajahDir = 'datawajah'
    latihDir = 'latihwajah'
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)
    faceDetector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faceRecognizer = cv2.face.LBPHFaceRecognizer_create()
    faceRecognizer.read(latihDir + '/training.xml')
    font = cv2.FONT_HERSHEY_SIMPLEX

    #id = 0
    yourname = entry1.get()
    names = []
    names.append(yourname)
    minWidth = 0.1 * cam.get(3)
    minHeight = 0.1 * cam.get(4)

    while True:
        retV, frame = cam.read()
        frame = cv2.flip(frame, 1)
        abuabu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceDetector.detectMultiScale(abuabu, 1.2, 5, minSize=(round(minWidth), round(minHeight)), )
        for (x, y, w, h) in faces:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0),2)
            id, confidence = faceRecognizer.predict(abuabu[y:y+h,x:x+w])
            if (confidence < 100):
                id = names[0]
                confidence = "  {0}%".format(round(150 - confidence))
            elif confidence < 50:
                id = names[0]
                confidence = "  {0}%".format(round(170 - confidence))

            elif confidence > 70:
                id = "Tidak Diketahui"
                confidence = "  {0}%".format(round(150 - confidence))

            cv2.putText(frame, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(frame, str(confidence), (x + 5, y + h + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        cv2.imshow('ABSENSI WAJAH', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # jika menekan tombol q akan berhenti
            break
    markAttendance(id)
    selesai3()
    cam.release()
    cv2.destroyAllWindows()

# GUI

# GUI
# Tambahan styling lebih modern
from tkinter import ttk

root = tk.Tk()
root.title("YehudaYura")
root.geometry("800x500")
root.configure(bg="#f0f8ff")  # Warna background soft

# Canvas
canvas = tk.Canvas(root, width=800, height=500, bg="#f0f8ff", highlightthickness=0)
canvas.grid(columnspan=3, rowspan=8)

# Judul dengan font modern
judul = tk.Label(root, text="Absensi Wajah", font=("Arial Rounded MT Bold", 30), bg="#005b96", fg="white", padx=10, pady=10)
canvas.create_window(400, 60, window=judul)

# Entry Nama
label1 = tk.Label(root, text="Nama Siswa", font=("Roboto", 14), fg="#333333", bg="#f0f8ff")
canvas.create_window(150, 150, window=label1)
entry1 = ttk.Entry(root, font="Roboto")
canvas.create_window(550, 150, height=25, width=400, window=entry1)

# Entry NIM
label2 = tk.Label(root, text="NIM", font=("Roboto", 14), fg="#333333", bg="#f0f8ff")
canvas.create_window(150, 200, window=label2)
entry2 = ttk.Entry(root, font="Roboto")
canvas.create_window(550, 200, height=25, width=400, window=entry2)

# Entry Kelas
label3 = tk.Label(root, text="Kelas", font=("Roboto", 14), fg="#333333", bg="#f0f8ff")
canvas.create_window(150, 250, window=label3)
entry3 = ttk.Entry(root, font="Roboto")
canvas.create_window(550, 250, height=25, width=400, window=entry3)

# Welcome Message
global instructions
instructions = tk.Label(root, text="absensi wajah mahasiswa", font=("Roboto", 15), fg="#003366", bg="#e6f7ff")
canvas.create_window(350, 300, window=instructions)

# Button Rekam Data
Rekam_text = tk.StringVar()
Rekam_btn = tk.Button(root, textvariable=Rekam_text, font="Roboto", bg="#0066cc", fg="white", height=1, width=15, command=rekamDataWajah)
Rekam_text.set("Scan Wajah")
Rekam_btn.grid(column=0, row=7)

# Button Training Wajah
Rekam_text1 = tk.StringVar()
Rekam_btn1 = tk.Button(root, textvariable=Rekam_text1, font="Roboto", bg="#0066cc", fg="white", height=1, width=15, command=trainingWajah)
Rekam_text1.set("Latih Wajah")
Rekam_btn1.grid(column=1, row=7)

# Button Absensi Wajah
Rekam_text2 = tk.StringVar()
Rekam_btn2 = tk.Button(root, textvariable=Rekam_text2, font="Roboto", bg="#0066cc", fg="white", height=1, width=20, command=absensiWajah)
Rekam_text2.set("Absensi")
Rekam_btn2.grid(column=2, row=7)

root.mainloop()
