import pymysql
from flask import Flask
 
app = Flask(__name__)
 
def getDate():    
        
    db = pymysql.connect(
        user='root', 
        passwd='1107!', 
        host='localhost', 
        db='pollu'
    )
    cursor = db.cursor()
    
    sql = f"""
           select distinct date from pollu.label_float_bbox
            """
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    DateList = []
    list = []
    for row in rows:
        list.append(row)
    
    for i in range(len(list)):
        DateList.append(list[i][0])

    db.close()
    return DateList

def getOptionList(date):    
        
    db = pymysql.connect(
        user='root', 
        passwd='1107!', 
        host='localhost', 
        db='pollu'
    )
    
    if date=='all':
        cursor = db.cursor()
    
        sql = f"""
            SELECT @rownum:=@rownum+1 as num, b.imagePath FROM (select distinct date, imagePath from pollu.label_float_bbox)as b WHERE (@rownum:=0)=0;
                """
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        ImagePathList = []
        for row in rows:
            ImagePathList.append(row)

        db.close()
        return ImagePathList
    else:
        cursor = db.cursor()
        
        sql = f"""
            SELECT @rownum:=@rownum+1 as num, b.imagePath FROM (select distinct date, imagePath from pollu.label_float_bbox)as b WHERE (@rownum:=0)=0 and date="{date}"
                """
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        ImagePathList = []
        for row in rows:
            ImagePathList.append(row)

        db.close()
        return ImagePathList

def getPositionList(ImagePath):  
        
    db = pymysql.connect(
        user='root', 
        passwd='1107!', 
        host='localhost', 
        db='pollu'
    )
    cursor = db.cursor()
    cursor1 = db.cursor()
    cursor2 = db.cursor()
    cursor3 = db.cursor()
    
    sql = f"""
           select label, up_left_x, up_left_y, bot_right_x, bot_right_y from  pollu.label_float_bbox where imagePath="{ImagePath}";
            """
    sql1 = f"""
        select distinct date from  pollu.label_float_bbox where imagePath="{ImagePath}";
        """   
    sql2 = f"""
        select distinct imageHeight, imageWidth from pollu.label_float_bbox where imagePath="{ImagePath}";
        """
    sql3 = f"""
           select label from  pollu.label_float_bbox where imagePath="{ImagePath}";
            """
    
    cursor.execute(sql)
    cursor1.execute(sql1)
    cursor2.execute(sql2)
    cursor3.execute(sql3)
    rows = cursor.fetchall()
    date = cursor1.fetchall()
    ImageSize = cursor2.fetchall()
    Label = cursor3.fetchall()
    
    LocationList = []
    for row in rows:
        LocationList.append(row)
        
    date = date[0][0]
    
    ImageHeight = ImageSize[0][0]
    ImageWidth = ImageSize[0][1]
    
    LabelList = []
    for i in range(len(Label)):
        LabelList.append(Label[i][0])

    db.close()
    return LocationList, date, ImageHeight, ImageWidth, LabelList

def getLabelList(Label):  
        
    db = pymysql.connect(
        user='root', 
        passwd='1107!', 
        host='localhost', 
        db='pollu'
    )
    cursor = db.cursor()
    
    sql = f"""
           SELECT @rownum:=@rownum+1 as num, b.imagePath FROM (select distinct label, imagePath from pollu.label_float_bbox)as b WHERE (@rownum:=0)=0 and label="{Label}";
            """
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    LabelList = []
    for row in rows:
        LabelList.append(row)

    db.close()
    return LabelList
 
if __name__ == '__main__':
    app.run(debug=True)
