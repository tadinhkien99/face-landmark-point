import cv2
import numpy as np

src=cv2.imread('FrontalFace-adv/primary_image_path/10000/00000IMG00000BURST2019123117241401448013org.jpg')


cv2.circle(src,(681,404), 3, (0,190,255),-1)
cv2.circle(src,(620,412), 3, (0,190,255),-1)
# cv2.circle(src,(2,1), 3, (0,190,255),-1)
# cv2.circle(src,(1,2), 3, (0,190,255),-1)

# cv2.circle(src,(820,394), 2, (0,190,255),-1)
# cv2.circle(src,(145,186), 2, (0,190,255),-1)
# cv2.circle(src,(156,196), 2, (0,190,255),-1)
# cv2.circle(src,(98,207), 2, (0,190,255),-1)

# cv2.circle(src,(106,194), 2, (0,190,255),-1)
# cv2.circle(src,(120,193), 2, (0,190,255),-1)
# cv2.circle(src,(135,193), 2, (0,190,255),-1)
# cv2.circle(src,(147,195), 2, (0,190,255),-1)
#
#
# #nose
# cv2.circle(src,(184,211), 2, (0,190,255),-1)
# cv2.circle(src,(190,233), 2, (0,190,255),-1)
# cv2.circle(src,(195,255), 2, (0,190,255),-1)
# cv2.circle(src,(201,277), 2, (0,190,255),-1)
#
# cv2.circle(src,(209,290), 2, (0,190,255),-1)
# cv2.circle(src,(195,290), 2, (0,190,255),-1)
# cv2.circle(src,(174,290), 2, (0,190,255),-1)
# cv2.circle(src,(170,278), 2, (0,190,255),-1)
#
# cv2.circle(src,(220,279), 2, (0,190,255),-1)
# cv2.circle(src,(237,268), 2, (0,190,255),-1)
# cv2.circle(src,(227,258), 2, (0,190,255),-1)
#
# cv2.circle(src,(243,379), 5, (0,190,255),-1)
# cv2.circle(src,(145,88), 5, (0,190,255),-1)

src = cv2.resize(src, (640,880))
# cv2.imwrite("asfaf.jpg", src)
cv2.imshow("src", src)
cv2.waitKey(0)