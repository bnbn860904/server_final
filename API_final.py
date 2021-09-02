from flask import Flask, send_file ,send_from_directory
from flask import jsonify, request
import numpy as np
from flask_cors import CORS
import io
import os
import json
import zipfile

import AI_series
import CV
import TMB_Semi_automated
import post_get
import TMB_Semi_automated_noDraw
import DB_AI 

app = Flask(__name__)
CORS(app)


series_gb = 0

@app.route("/")
def hello():
    return "Hello!"

       
@app.route('/AI_series', methods=['GET']) ## tumor_segmentation(AI)
def AI_ser():
    
    global series_gb
    global series_coordinate
    global name_gb
    
    if 'number' in request.args:
        number = request.args['number']
        
        patient_id    = number.split('-')
        print(patient_id)
        study_id      = patient_id[1]
        series_id     = patient_id[3]
        instance_id   = patient_id[5] + '.dcm'
        print(series_gb)
        if(series_id == series_gb):
            imgNum = []
            try:
                index             = name_gb.index(instance_id)
                result            = series_coordinate[index]
                print(index)
                print(result)
                result = (result).tolist()
                A_list = []
                k = len(result)
                for i in range(0, k):     
                    A_list += result[i]                 
                print('other2')
            except:
                result            = []            
                print('other3')
            
        else:
            series_gb         = series_id
            series_id         = post_get.DicomRequests(series_id) #post&get
            image_path        = "./" + series_id + "/"            #image_path        = "./" + study_id + "/" + series_id + "/"            
            name,coor,imgNum  = AI_series.main(image_path)
            series_coordinate = coor
            name_gb           = name
            print(imgNum)
            try:
                index             = name.index(instance_id)
                result            = coor[index]
                result = (result).tolist()
                A_list = []
                k = len(result)
                for i in range(0, k):     
                    A_list += result[i]  
                print('first')
            except:
                result            = []
                print('first')
    else:
        print("error")
       
    patient = {
        "liver":result,
        "imgNum":imgNum
     }     
    
    return jsonify(patient)

        
@app.route('/tumorCV', methods=['GET'])  ## tumor_segmentation(CV)
def CV_seg():
    results = []
    
    str_url = ""
    
    if 'number' in request.args:
        number = request.args['number']
        
        str_url      = number.split('-')
        study_id     = str_url[1]
        series_id    = str_url[3]
        instance_id  = str_url[5]
        coordinate   = int(str_url[6]),int(str_url[7])
        print(coordinate)
        image_path   = './' + series_id + '/' + instance_id #image_path   = './' + study_id + '/' + series_id + '/' + instance_id 
        
    else:
        print("error")
     
    series_id  = post_get.DicomRequests(series_id) #post&get
    cv_contours = CV.region_growing_API(image_path, coordinate)
    
    cv_contours = (cv_contours).tolist()
    B_list = []
    k = len(cv_contours)
    for i in range(0, k):
        if i % 5 == 0:  
            B_list += cv_contours[i]            
    
    print('B_list',B_list)
    patient2 = {
        
    #"coordinate":[[140,110],[140,111]]
    "coordinate": B_list    
     }
       
    return jsonify(patient2)


@app.route('/3D_top', methods=['GET'])  ## 3D_top_segmentation
def top():
    results = []
    
    str_url = ""
    
    global coordinate_top
    global instance_top
    
    if 'number' in request.args:
        number = request.args['number']
        str_url = number.split('-')
        coordinate_top = str_url
        
        
    if 'patient_id' in request.args:
        patient_id = request.args['patient_id']
        
        str_url       = patient_id.split('-')
        study_id      = str_url[1]
        series_id     = str_url[3]
        instance_top  = str_url[5]
        
    mytest = {
    
     }
       
    return jsonify(mytest)


@app.route('/3D_middle', methods=['GET'])  ## 3D_middle_segmentation
def middle():
    results = []
    
    str_url = ""
    
    global coordinate_mid
    global WL
    global D3_image_path
    global instance_mid
    
    if 'number' in request.args:
        number = request.args['number']
        str_url = number.split('-')
        coordinate_mid = str_url
        
        #print(str_url)
        
    if 'patient_id' in request.args:
        patient_id = request.args['patient_id']
        
        str_url       = patient_id.split('-')
        study_id      = str_url[1]
        series_id     = str_url[3]
        instance_mid  = str_url[5]
        series_id     = post_get.DicomRequests(series_id) #post&get
        D3_image_path   = './' + series_id + '/'#D3_image_path   = './' + study_id + '/' + series_id + '/'
        
    if 'WL' in request.args:
        WL_list = request.args['WL']
        WL = WL_list.split('-')
        
        
    mytest = {
    
     }
       
    return jsonify(mytest)


@app.route('/3D_bottom', methods=['GET'])  ## 3D_bottom_segmentation
def bottom():
    results = []
    
    str_url = ""
    
    global coordinate_bot
    global instance_bot
    
    if 'number' in request.args:
        number = request.args['number']
        str_url = number.split('-')
        coordinate_bot = str_url
        
    if 'patient_id' in request.args:
        patient_id = request.args['patient_id']
        
        str_url       = patient_id.split('-')
        study_id      = str_url[1]
        series_id     = str_url[3]
        instance_bot  = str_url[5]
        
    mytest = {
    
     }
       
    return jsonify(mytest)

@app.route('/start_drawing', methods=['GET'])  ## start_drawing
def start():
        
    top = xy_array(coordinate_top)
    print(top)
    mid = xy_array(coordinate_mid)
    print(mid)
    bot = xy_array(coordinate_bot)
    print(bot)
    
    print(WL)
    L = int(WL[0])
    W = int(WL[1])
    
    #input_file = TMB_Semi_automated.main('C:/Users/leowang/Desktop/00A00101/', 'C:/Users/leowang/Desktop/test/',L, W, '00A00101_3_07', top, '00A00101_3_13', mid, '00A00101_3_30', bot)
    D3_contours = TMB_Semi_automated.main( D3_image_path, './tmb_png/', L, W, instance_top, top, instance_mid, mid, instance_bot, bot)
    com_line = 'pvpython png2vti.py --input ' + D3_contours + ' --output volume99'
    os.system(com_line)
    
    mytest = {
    
     }
       
    return jsonify(mytest)  

@app.route('/draw_back', methods=['GET'])  ## draw_back
def draw_back():
        
    top = xy_array(coordinate_top)
    #print(top)
    mid = xy_array(coordinate_mid)
    #print(mid)
    bot = xy_array(coordinate_bot)
    #print(bot)
    
    #print(WL)
    L = int(WL[0])
    W = int(WL[1])
    
    if 'number' in request.args:
        number = request.args['number']
        
    instance_id   = number + '.dcm' 
    print(instance_id)
    
    D3_contours, dcm_name_list = TMB_Semi_automated_noDraw.main( D3_image_path, './tmb_png/', L, W, instance_top, top, instance_mid, mid, instance_bot, bot)
    
    try:
        index             = dcm_name_list.index(instance_id)
        result            = D3_contours[index]
        result            = (result).tolist()
    except:
        result = []
    
    print(dcm_name_list)
    print(D3_contours)
    mytest = {
        "coordinate": result
     }
       
    return jsonify(mytest) 
    
def xy_array(a_list):  
    A = []
    k = len(a_list)
    for i in range(0, k-2,2):
        #print(i)
        A.append([int(a_list[i]),int(a_list[i+1])])
                
    return A  

@app.route('/dcm2vti', methods=['GET'])
def dcm2vti():
    
    if 'number' in request.args:
        number = request.args['number']
        
        str_url      = number.split('-')
        study_id     = str_url[1]
        series_id    = str_url[3]
        series_id    = post_get.DicomRequests(series_id) #post&get
        image_path   = './' + series_id + '/' #image_path   = './' + study_id + '/' + series_id + '/' 
        
        com_line = 'pvpython dcm2vti.py --input ' + image_path + ' --output ' + series_id
        os.system(com_line)
            
    mytest = {"series_id": series_id}
    return jsonify(mytest)
        
    
@app.route('/upload_3D', methods=['GET'])
def upload_3D():

    if 'number' in request.args:
        number   = request.args['number']    
        vti_path = "./vti/" + number + ".vti"
        
    with open(vti_path, 'rb') as bites:
        return send_file(
            io.BytesIO(bites.read()),
            mimetype='image/vti'
        )
    
@app.route('/upload', methods=['GET'])
def upload():

    if 'number' in request.args:
        number   = request.args['number']    
        vti_path = "./tmb_vti/" + number + ".vti"
        
    with open(vti_path, 'rb') as bites:
        return send_file(
            io.BytesIO(bites.read()),
            mimetype='image/vti'
        )        
 
@app.route('/pre_upload', methods=['GET'])
def pre_upload():
    
    if 'number' in request.args:
        number = request.args['number']
        
        str_url      = number.split('-')
        study_id     = str_url[1]
        series_id    = str_url[3] 
        print(series_id)
        series_id = post_get.DicomRequests(series_id)
        
    mytest = {}
    return jsonify(mytest) 

 
@app.route('/post_coor', methods=['POST','GET'])
def post_coor():
     
     points = []
     if request.method == 'POST':
        number       = request.args['number']
        str_url      = number.split('-')
        series_id    = str_url[0]
        instance_id  = str_url[1]
        coor         = json.loads(request.data)
        
        for x in range(0, len(coor['data'])):
            points.append(coor['data'][x]['handles']['points'])
        
        color = coor['data'][0]['color']

        try:
            os.mkdir('./coordinate/' + series_id)
        except:
            print('FileExists')  
        with open('./coordinate/' + series_id + '/' + instance_id + '.json', 'w+') as fp:
            try:
                data = json.load(fp)
                data[color]['uuid'] = coor['data'][0]['uuid']
                data[color]['points'] = points
                print('old')
                
            except:
                data = {}
                data[color] = {}
                data[color]['uuid'] = coor['data'][0]['uuid']
                data[color]['points'] = points
                print('new')                
                
            json.dump(data, fp, indent=4)                
       
        return 'Hello 123'
 
@app.route('/download_singleCV', methods=['GET'])
def download_singleCV():
    
    if 'number' in request.args:
        number = request.args['number']
        str_url      = number.split('-')
        series_id    = str_url[0]
        instance_id  = str_url[1]
    
    CV_path = 'coordinate' + '/' + series_id   
    return send_from_directory(CV_path, instance_id + '.json', as_attachment=True)
 
@app.route('/download_series', methods=['GET'])
def download_series():
    
    if 'number' in request.args:
        number = request.args['number']
        str_url      = number.split('-')
        series_id    = str_url[0]
        instance_id  = str_url[1]
        
    CV_path = 'coordinate' + '/' + series_id        
    def zip_dir(path):
        zf = zipfile.ZipFile('{}.zip'.format(path), 'w', zipfile.ZIP_DEFLATED)
       
        for root, dirs, files in os.walk(path):
            for file_name in files:
                zf.write(os.path.join(root, file_name))
    print(series_id)        
    zip_dir(CV_path)       
    return send_from_directory('coordinate', series_id + '.zip', as_attachment=True)

 
@app.route('/Pre_execute_AI', methods=['GET'])
def Pre_execute_AI():
    
    if 'number' in request.args:
        number = request.args['number']
        #str_url      = number.split('-')
        series_id    = number
        
        image_path        = "./" + series_id + "/"                
        ID, coor, imgNum  = AI_series.main(image_path)
        print("ID is",ID)
        print("coor is",coor)
        o                 = DB_AI.DB_AI_store(ID,coor)
        
    patient = {
        
     }     
    
    return jsonify(patient)
        
 
@app.route('/DB_AI_get', methods=['GET'])
def DB_AI_get():
    
    if 'number' in request.args:
        number = request.args['number']
        instance_id    = number + '.dcm'
        
        result         = DB_AI.DB_AI_get(instance_id)
        
    patient = {
        "liver":result,
     }     
    
    return jsonify(patient)
    
if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)    
    