import numpy as np
import cv2

from utils import CFEVideoConf, image_resize

cap = cv2.VideoCapture(0)

save_path = '/home/vatsal/PycharmProjects/Watermark/Test.mp4'
frames_per_seconds = 24
config = CFEVideoConf(cap, filepath=save_path, res='720p')
out = cv2.VideoWriter(save_path, config.video_type, frames_per_seconds, config.dims)

img_path = '/home/vatsal/PycharmProjects/Watermark/safehalo.png'
logo = cv2.imread(img_path, -1)
watermark = image_resize(logo, height=50)
watermark = cv2.cvtColor(watermark, cv2.COLOR_BGR2BGRA)

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    frame_h, frame_w, frame_c = frame.shape
    # print(frame.shape)

    # overlay with 4 channels BGR and Alpha
    overlay = np.zeros((frame_h, frame_w, 4), dtype='uint8')
    watermark_h, watermark_w, watermark_c = watermark.shape
    cv2.putText(frame,"safehalo",(50,20),cv2.FONT_HERSHEY_SIMPLEX,5,(255,50,50),4)
    for i in range(0, watermark_h):
        for j in range(0, watermark_w):
            # print(watermark[i,j])
            if watermark[i, j][3] != 0:
                # watermark[i, j] # RBGA
                offset = 10
                h_offset = frame_h - watermark_h - offset
                w_offset = frame_w - watermark_w - offset
                overlay[h_offset + i, w_offset + j] = watermark[i, j]

    cv2.addWeighted(overlay, 0.25, frame, 1.0, 0, frame)


    # frame.addimage(watermark)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    out.write(frame)
    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break


# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()
