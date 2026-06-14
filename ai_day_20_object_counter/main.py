import cv2
import numpy as np
import sys
from pathlib import Path

def count_objects(image_path, min_area=500):
    img  = cv2.imread(image_path)
    if img is None:
        print(f"Cannot load: {image_path}"); return
    gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur  = cv2.GaussianBlur(gray, (5,5), 0)
    edges = cv2.Canny(blur, 50, 150)
    kernel   = np.ones((3,3), np.uint8)
    dilated  = cv2.dilate(edges, kernel, iterations=2)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    valid    = [c for c in contours if cv2.contourArea(c) >= min_area]
    output   = img.copy()
    for i, c in enumerate(valid):
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(output,str(i+1),(x+5,y+20),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),2)
        area = cv2.contourArea(c)
    cv2.putText(output,f"Objects: {len(valid)}",(10,35),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
    out_path = Path(image_path).stem + "_counted.jpg"
    cv2.imwrite(out_path, output)
    print(f"\n  Objects detected : {len(valid)}")
    print(f"  Output saved     : {out_path}")
    for i, c in enumerate(valid):
        x,y,w,h = cv2.boundingRect(c)
        area = cv2.contourArea(c)
        print(f"  Object {i+1}: position ({x},{y}), size {w}x{h}, area {area:.0f}px")
    cv2.imshow("Object Counter", output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    print("=== Object Counter ===")
    if len(sys.argv) > 1:
        min_area = int(input("Min object area in pixels (default 500): ") or 500)
        count_objects(sys.argv[1], min_area)
    else:
        while True:
            print("\n1. Count objects in image  2. Quit")
            c = input("Choice: ").strip()
            if c == "1":
                path     = input("Image path: ").strip()
                min_area = int(input("Min area (default 500): ") or 500)
                count_objects(path, min_area)
            elif c == "2":
                break

if __name__ == "__main__":
    main()
