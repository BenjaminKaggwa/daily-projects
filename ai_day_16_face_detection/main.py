import cv2
import sys
from pathlib import Path

def detect_faces(image_path, scale=1.1, neighbors=5, min_size=(30,30)):
    img  = cv2.imread(image_path)
    if img is None:
        print(f"Could not load image: {image_path}")
        return
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    detector     = cv2.CascadeClassifier(cascade_path)
    faces = detector.detectMultiScale(gray, scaleFactor=scale, minNeighbors=neighbors, minSize=min_size)
    print(f"\n  Faces detected : {len(faces)}")
    for i, (x, y, w, h) in enumerate(faces):
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(img, f"Face {i+1}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
        print(f"  Face {i+1}: position ({x},{y}), size {w}x{h}px")
    output = Path(image_path).stem + "_detected.jpg"
    cv2.imwrite(output, img)
    print(f"  Output saved : {output}")
    cv2.imshow("Face Detection", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    print("=== Face Detection App ===")
    if len(sys.argv) > 1:
        detect_faces(sys.argv[1])
    else:
        while True:
            print("\n1. Detect faces in image  2. Use webcam  3. Quit")
            c = input("Choice: ").strip()
            if c == "1":
                path = input("Image path: ").strip()
                detect_faces(path)
            elif c == "2":
                print("Starting webcam (press Q to quit)...")
                cap      = cv2.VideoCapture(0)
                cascade  = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
                while True:
                    ret, frame = cap.read()
                    if not ret: break
                    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = cascade.detectMultiScale(gray, 1.1, 5)
                    for (x,y,w,h) in faces:
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                        cv2.putText(frame,f"Face",(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),2)
                    cv2.putText(frame,f"Faces: {len(faces)}",(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                    cv2.imshow("Face Detection", frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"): break
                cap.release()
                cv2.destroyAllWindows()
            elif c == "3":
                break

if __name__ == "__main__":
    main()
