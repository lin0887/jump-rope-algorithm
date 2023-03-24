import pandas as pd
import numpy as np
import statistics

class Body_point:

    def __init__(self,post_df = pd.DataFrame ,point = 11):
        
        self.data = post_df[int(point+33)]
        self.frame_num = len(self.data)
        self.frame = range(self.frame_num)
        self.var = 2.5
        self.average_wavelength = 0


    def get_amplitude(self):
        
        self.L_maximum = []
        self.R_maximum = []
        self.minimum = []
        self.amplitude = []
        self.wavelength = []
        self.dobule_amplitude = []
        
        # 找出所有區間極值，並過濾偽區間極值
        max_tmp = []
        min_tmp = []
        for i in range(1,self.frame_num-1):
            if self.data[i-1] < self.data[i] and self.data[i+1]< self.data[i]:
                
                left = i - int(( self.average_wavelength / 2 ) )
                right = i + int(( self.average_wavelength / 2 ) )
                
                if 0 > left :
                    left = 0
                if right > self.frame_num :
                    right = self.frame_num   
                if self.average_wavelength == 0 :
                    right =  i+1
                
                if self.data[i] == np.max(self.data[left:right]):
                    max_tmp.append(i)
                    
            elif self.data[i-1]>self.data[i] and self.data[i+1]>self.data[i]:
                
                left = i - int(( self.average_wavelength * 0.3) )
                right = i + int(( self.average_wavelength *0.3 ) )
                
                if 0 > left :
                    left = 0
                if right > self.frame_num :
                    right = self.frame_num   
                if self.average_wavelength == 0 :
                    right =  i+1    
                
                if self.data[i] == np.min(self.data[left:right]) :
                    min_tmp.append(i)
                
        # 找出所有的波、振幅、波長  
        i = 0
        j = 0
        k = 1
        minsize = len(min_tmp)
        maxsize = len(max_tmp)
        while i != minsize and j+k != maxsize:
            if  max_tmp[j] < min_tmp[i] < max_tmp[j+k] :           
                self.minimum.append(min_tmp[i])
                self.L_maximum.append(max_tmp[j])
                self.R_maximum.append(max_tmp[j+k])
                self.amplitude.append(np.min( [self.data[max_tmp[j]]-self.data[min_tmp[i]],
                                            self.data[max_tmp[j+k]]-self.data[min_tmp[i]] ]))
                self.dobule_amplitude.append(self.data[max_tmp[j]]-self.data[min_tmp[i]]+
                                self.data[max_tmp[j+k]]-self.data[min_tmp[i]] )
                self.wavelength.append(max_tmp[j+k]-max_tmp[j]+1)
                i += 1
                j += k                      
            elif max_tmp[j] > min_tmp[i]:
                i += 1
            else:
                j += 1     

        #print(len(self.amplitude))
        # 正規化振幅，並分段
        self.normalization_amplitude = self.amplitude/np.linalg.norm(self.amplitude)
        self.section_normalization_amplitude = []
        tmp2 = []
        for i in self.normalization_amplitude:
            if i > 0.05:
                num = round(i+0.025, 3)
                if num - round(num,1) < 0.05:
                    num = round(num,1)
                else:
                    num = round(num,1) + 0.5
                self.section_normalization_amplitude.append(num)
                tmp2.append(num)
            else:
                self.section_normalization_amplitude.append(0)
       
        #　取振幅眾數
        self.mode_amplitude = statistics.mode(tmp2)

        # 取振幅眾數平均數
        tmp = []
        for i in range(len(self.section_normalization_amplitude)):
            if self.section_normalization_amplitude[i] == self.mode_amplitude:
                tmp.append(self.amplitude[i])
        self.average_amplitude = np.mean(tmp)
        
        # 取振幅標準差
        self.std_amplitude = np.std(tmp, ddof=1)
        
        # 取振幅區間
        self.amplitude_upper_bound = self.average_amplitude + self.std_amplitude * self.var
        self.amplitude_lower_bound = self.average_amplitude - self.std_amplitude * self.var
        
        
    def get_wavelength(self):

        # 取波長平均數
        tmp = []
        for idx in range(len(self.section_normalization_amplitude)):
            if self.section_normalization_amplitude[idx] == self.mode_amplitude:
                tmp.append(self.wavelength[idx])      
        self.average_wavelength = int( np.mean(tmp) + 0.5 )
        
        # 取波長區間
        self.wavelength_upper_bound = int(self.average_wavelength  * 1.5 + 0.5 )
        self.wavelength_lower_bound = int(self.average_wavelength  * 0.5 + 0.5 ) 
        #print(self.wavelength_upper_bound,self.wavelength_lower_bound,int(self.average_wavelength))


    def jump_rope_count(self):

        times = 0
        self.flag = []
        for i in range(len(self.minimum)):
            if self.dobule_amplitude[i] >= self.average_amplitude * 0.7 :
                if self.wavelength_lower_bound <= self.wavelength[i] <= self.wavelength_upper_bound:
                    self.flag.append(2)
                    times += 1
                else:
                    self.flag.append(1)
            else :
                self.flag.append(0)
       
        return times
    
    def make_flag(self):
          
        f = [0]*self.frame_num
               
        for i in range(len(self.minimum)):
            if self.flag[i] == 2:
                f[self.minimum[i]] = 1
        
        return f
            
              
        
    


if __name__=="__main__":

    a = Body_point('A1103.csv',11)
    for i in range(2):
        a.get_amplitude()
        a.get_wavelength()
    ans = a.jump_rope_count()  
    
   
    
