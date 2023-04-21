import pandas as pd
import os

def judgment_grade(data):
    grade_award_map = {
        '一年級': {50: '金質獎', 40: '銀質獎', 30: '銅質獎'},
        '二年級': {80: '金質獎', 60: '銀質獎', 40: '銅質獎'},
        '三年級': {95: '金質獎', 90: '銀質獎', 85: '銅質獎'},
        '四年級': {100: '金質獎', 95: '銀質獎', 90: '銅質獎'},
        '五年級': {50: '金質獎', 45: '銀質獎', 40: '銅質獎'},
        '六年級': {55: '金質獎', 50: '銀質獎', 45: '銅質獎'},
        '推廣組': {70: '金質獎', 50: '銀質獎', 30: '銅質獎'},
        '特教組': {70: '金質獎', 50: '銀質獎', 30: '銅質獎'}
    }
    grade = data['年級']
    score = data['成績']
    
    if grade in grade_award_map and score in grade_award_map[grade]:
        return grade_award_map[grade][score]
    else:
        return None

def student():
    df = pd.read_json('..\\Backend\\contestants.json')
    for i in range( len(df) ):
        k = judgment_grade(df.loc[i,:])
        df.loc[i , '等第'] = k
        
    df.to_excel('..\\名單\\112跳繩各校學生成績.xlsx',index=False)
    
    df.drop(columns=['組別','成績','ID'])
    
    new_order = ['年級', '學校', '項目', '等第', '姓名', '指導老師']
    df = df.reindex(columns=new_order)
    df.columns = ['參賽組別', '單位', '項目', '成績', '優秀選手', '指導老師']
    
    df.dropna(subset=['成績'], inplace=True)
    df['項目']=['單人繩' for i in range(len(df))]    
    df['參賽組別'] = df['參賽組別'].apply(lambda x: x + '組')     
          
    df.to_excel('..\\名單\\112跳繩各校學生獎狀.xlsx',index=False)
    
def teacher():
    
    df = pd.read_excel('..\\名單\\112跳繩各校學生成績.xlsx')
    
    # 找出所有等第非None的row
    df = df.dropna(subset=['等第'])

    # 按指導老師分組
    groups = df.groupby(['指導老師'])

    new_rows = []

    # 遍歷每個指導老師的分組
    for name, group in groups:
        # 按年級和組別分出不同年級和男女組
        grade_groups = group.groupby(['年級', '組別'])
        
        # 選擇每個年級和組別中的最高成績
        for gname, ggroup in grade_groups:
            max_row = ggroup.loc[ggroup['成績'].idxmax()]
            new_rows.append(max_row)

    # 建立新的dataframe
    new_df = pd.DataFrame(new_rows, columns=df.columns)
    
    # 製作輸出格式
    new_df.drop(columns=['組別','成績','ID'])
    new_order = ['年級', '學校', '項目', '等第', '姓名', '指導老師']
    new_df = new_df.reindex(columns=new_order)
    new_df.columns = ['參賽組別', '單位', '項目', '成績', '優秀選手', '指導老師']
    new_df['項目']=['單人繩' for i in range(len(new_df))]    
    new_df['參賽組別'] = new_df['參賽組別'].apply(lambda x: x + '組') 
    
    new_df.to_excel('..\\名單\\112跳繩各校老師獎狀.xlsx',index=False)
    
if __name__ == '__main__':
    check()
    #student()
    teacher()
    
    
