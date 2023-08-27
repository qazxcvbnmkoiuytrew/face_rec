import cv2

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_color = (0, 255, 0) 
video_capture=cv2.VideoCapture(0) #初始化鏡頭，0表示第一個鏡頭

i=0;
while True: #進入無限循環，持續從攝像頭讀取畫面。
    ret,frame=video_capture.read() #ret表示是否成功讀取，frame為畫面數值
    frame = cv2.flip(frame,1) # 1表示沿著 y 軸翻轉（左右翻轉）、0表示沿著 x 軸翻轉（上下翻轉）、-1表示x,y同時翻轉
    cv2.imshow('Horizontally Video',frame) #video為視窗標題

    if cv2.waitKey(5)&0xFF==ord('q'): #按q跳出
        break;
    elif cv2.waitKey(5)&0xFF==ord('s'):
        i=i+1;
        resized_frame = cv2.resize(frame,(640,480))
        text = "Hello"
        cv2.putText(resized_frame, text, (10, 30), font, font_scale, font_color, 2)
        cv2.imshow('Captured Image', resized_frame)
        cv2.imwrite('picture'+str(i)+'.jpg', frame) #將畫面 frame 保存為 "picturei.jpg" 的圖像文件，其中 i 是圖像編號。
        print('save','picture'+str(i)+'.jpg') #在控制台輸出保存的圖像文件名。
                                
video_capture.release() #釋放攝像頭資源。
cv2.destroyAllWindows() #關閉所有視窗。
