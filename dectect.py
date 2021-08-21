from anpr import DetectANPR
from imutils import paths
import imutils
import cv2
import re

anpr= DetectANPR(debug=True)
imagePaths= sorted(list(paths.list_images("ProyectoCGV/images/")))
print(imagePaths)

for path in imagePaths:
    image = cv2.imread(path)
    image = imutils.resize(image,width=600)
    (lpText,lpCnt)= anpr.find_and_ocr(image,psm=7,clearBorder=True)
    if lpText is not None:
        box = cv2.boxPoints(cv2.minAreaRect(lpCnt))
        box = box.astype("int")
        cv2.drawContours(image,[box],-1,(0,255,0),1)
        (x,y,w,h)=cv2.boundingRect(lpCnt)
        cv2.putText(image, re.sub(r"[\W_]+","",lpText), (x, y - 15),
          cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        print("[INFO] {}".format(lpText))
        cv2.imshow("Output ANPR", image)
        cv2.waitKey(0)
  