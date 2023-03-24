import cv2
import mediapipe as mp
import pandas as pd


class Post_dection:
    def __init__(self,video) -> None:
        #Init all file path
        self.file_path = video
        print(self.file_path)
        # Initialize mediapipe drawing class - to draw the landmarks points.
        self.mp_pose = mp.solutions.pose 
        
        
    def dection(self):
        
        # Init image data
        cap = cv2.VideoCapture(self.file_path)
        totle_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        idx = 0
        
        pose_landmark_data = []
        
        
        # 設定模型參數
        with self.mp_pose.Pose(static_image_mode=False, model_complexity=2, enable_segmentation=True, min_detection_confidence=0.5) as pose:
            while True:
                
                success, image = cap.read()
                if not success:
                    break
                
                # 呼叫姿勢追蹤API
                # 在處理之前將 BGR 圖像轉換為 RGB
                results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                
                if results.pose_landmarks is not None: 
                    
                    # make pose landmark data
                    x = []
                    y = []
                    z = []
                    for i in self.mp_pose.PoseLandmark:
                        x.append (results.pose_landmarks.landmark[i].x)
                        y.append (results.pose_landmarks.landmark[i].y)
                        z.append (results.pose_landmarks.landmark[i].z)
                    pose_landmark_data.append(x + y + z)

                else :
                    
                    if len(pose_landmark_data) != 0 :
                        pose_landmark_data.append(self.pose_landmark_data[-1])
                       
                print('\rprocess: {}/{}'.format(idx+1,totle_frames), end = ' ')
                idx += 1
        
        pose_landmark_df = pd.DataFrame(pose_landmark_data)
        return pose_landmark_df
            
    def make_output_vidoe(self,output_path,flag):  
        
    
        # Init image data
        cap = cv2.VideoCapture(self.file_path)
        totle_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out_video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
        
        
        # Initialize mediapipe drawing class - to draw the landmarks points.
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
       
        
        
        idx = 0
        count = 0
        # 設定模型參數
        with self.mp_pose.Pose(static_image_mode=False, model_complexity=2, enable_segmentation=True, min_detection_confidence=0.5) as pose:
            while True:
                # 將影片切割成圖片處理
                success, image = cap.read()
                
                if not success:
                    break
                
                # 呼叫姿勢追蹤API
                # 在處理之前將 BGR 圖像轉換為 RGB
                results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                annotated_image = image.copy()
                
                if flag[idx] == 1:
                    count += 1
                
            
                if results.pose_landmarks is not None:
                    
                    # 將關節畫在圖片上面
                    mp_drawing.draw_landmarks(
                            image = annotated_image,
                            landmark_list = results.pose_landmarks,
                            connections = self.mp_pose.POSE_CONNECTIONS,
                            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
                            )   
                     
                    cv2.putText(annotated_image, 'frame=' +str(idx), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.putText(annotated_image, 'count=' +str(count), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
                    
                out_video.write(annotated_image)
                
                print('\rprocess: {}/{}'.format(idx+1,totle_frames), end = ' ')
                idx += 1
                
            out_video.release()
              
    
if __name__ == '__main__':
    
    video = '.\\A1102.MOV'
    a = Post_dection(video)
    b = a.dection()
    