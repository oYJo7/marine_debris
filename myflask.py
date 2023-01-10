from flask import Flask, request
from flask import render_template
from myDB import getDate, getOptionList, getPositionList
 
app = Flask(__name__)
 
@app.route('/', methods =['get','post'])
def myindex():
    DateList=getDate()
    return render_template('index.html', DateList = DateList)

@app.route('/result', methods =['get','post'])
def myresult():
    date = request.form["date"]
    ImagePathList = getOptionList(date)
    return render_template('result.html', ImagePathList=ImagePathList)

@app.route('/detail', methods =['get','post'])
def mydetail():
    ImagePath = request.form["ImagePath"]
    LocationList, date, ImageHeight, ImageWidth, DetailLabelList = getPositionList(ImagePath)
    if ImageHeight == 800 and ImageWidth == 1200:
        ImageHeight = (ImageHeight//4)*3 #600
        ImageWidth = (ImageWidth//4)*3 #900
    else:
        ImageHeight = ImageHeight//4
        ImageWidth = ImageWidth//4
    SliceImagePath = ImagePath.split('_')
    SliceImagePath = SliceImagePath[1].split('.')
    SliceImagePath = int(SliceImagePath[0])
    print(SliceImagePath)
    return render_template('detail.html', SliceImagePath=SliceImagePath, ImagePath = ImagePath, LocationList=LocationList, date=date, ImageHeight=ImageHeight, ImageWidth=ImageWidth, DetailLabelList=DetailLabelList)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port='80', debug=True)