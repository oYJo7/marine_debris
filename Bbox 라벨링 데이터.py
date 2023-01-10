from ast import Continue
import json, pymysql, os

for z in range(1, 7, 1):
    #폴더 안에 파일 이름 리스트화
    file_list = os.listdir('H:\\123.해안 오염물질 데이터\\01.데이터\\1.Training\\라벨링데이터\\TL_부유쓰레기(Bbox)(원본)\\TL'+str(z))
    print(file_list)

    for k in range(0, len(file_list)):
        #json 파일 읽기
        with open('H:\\123.해안 오염물질 데이터\\01.데이터\\1.Training\\라벨링데이터\\TL_부유쓰레기(Bbox)(원본)\\TL'+str(z)+'\\'+file_list[k], 'r') as f:
            #json->dict
            json_data = json.load(f)
        print(k,' : ',file_list[k])

        #data1 = 원본 데이터에서 value 값만
        data1=[]

        for i in json_data:
            #flags 항목 제거
            if type(json_data.get(i))==dict:
                continue
            else:
                #dict에서 value 값 가져오기
                data1.append(json_data.get(i))

        #data2 = data1에서 인덱스 1번 값(shapes의 key/value 값)
        data2=data1[1]
        del data1[1]

        #data3 = data2에서 value 값만
        data3=[]
        for i in data2:
            for j in i:
                #flags 항목 제거
                if type(i.get(j))==dict:
                    continue
                else:
                    data3.append(i.get(j))
        
        count = 0
        if len(data3[-4])==2:
            #points: bbox 좌표 값만
            points=[]
            for i in range(1,len(data3),5):
                for j in data3[i]:
                    points.append(j)   
            count = 4
        elif len(data3[-3])==2:
            #points: bbox 좌표 값만
            points=[]
            for i in range(1,len(data3),4):
                for j in data3[i]:
                    points.append(j)
            count = 3
                                    
        for i in data3:
            if type(i)==list:
                del data3[data3.index(i)]

        #result: points에서 숫자값만 남기기
        result=[]
        for i in range(len(points)):
            for j in range(2):
                result.append(points[i][j])
        
                    

        con = pymysql.connect(host='localhost', user='root', password='1107!', db='pollu', charset='utf8')
        cur = con.cursor()
        
        if (len(data3)//4)+1 == 1 and count == 3:
            sql = "INSERT INTO pollu.label_float_bbox (up_left_x,up_left_y,bot_right_x,bot_right_y,label,origin,shape_type,version,imagePath,imageData,imageHeight,imageWidth,date,time,device,camera,shutter,altitude,lat,lon,gtype) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            cur.execute(sql, (result[0],result[1],result[2],result[3],data3[0],data3[1],data3[2],data1[0],data1[1],data1[2],data1[3],data1[4],data1[5],data1[6],data1[7],data1[8],data1[9],data1[10],data1[11],data1[12],data1[13]))
        elif count == 4:
            sql = "INSERT INTO pollu.label_float_bbox (up_left_x,up_left_y,bot_right_x,bot_right_y,label,origin,group_id,shape_type,version,imagePath,imageData,imageHeight,imageWidth,date,time,device,camera,shutter,altitude,lat,lon,gtype) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            for i in range(1,(len(data3)//4)+1):
                cur.execute(sql, (result[0],result[1],result[2],result[3],data3[0],data3[1],data3[2],data3[3],data1[0],data1[1],data1[2],data1[3],data1[4],data1[5],data1[6],data1[7],data1[8],data1[9],data1[10],data1[11],data1[12],data1[13]))
                del result[0]
                del result[0]
                del result[0]
                del result[0]
                del data3[0]
                del data3[0]
                del data3[0]
                del data3[0]
        elif count == 3:
            sql = "INSERT INTO pollu.label_float_bbox (up_left_x,up_left_y,bot_right_x,bot_right_y,label,origin,shape_type,version,imagePath,imageData,imageHeight,imageWidth,date,time,device,camera,shutter,altitude,lat,lon,gtype) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            for i in range(1,(len(data3)//3)+1):
                cur.execute(sql, (result[0],result[1],result[2],result[3],data3[0],data3[1],data3[2],data1[0],data1[1],data1[2],data1[3],data1[4],data1[5],data1[6],data1[7],data1[8],data1[9],data1[10],data1[11],data1[12],data1[13]))
                del result[0]
                del result[0]
                del result[0]
                del result[0]
                del data3[0]
                del data3[0]
                del data3[0]

        con.commit()
        #cur.fetchall() 
        con.close()
    