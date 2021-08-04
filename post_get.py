
def DicomRequests(seriesId):

    import os    
    if os.path.isdir("./" + seriesId):
        print(seriesId + "資料夾存在")
    else:
        print(seriesId + "資料夾不存在")
        import requests
        import json
        import zipfile
        from os.path import join
        import shutil
        import rename_SOPInstanceUID

        # 資料    
        my_data = seriesId
        headers = {'Content-Type':'application/json'}

        # 將資料加入 POST 請求中
        r = requests.post('http://localhost:8042/tools/lookup', data = my_data ,headers = headers)

        print((r.json()[0])['ID'])
        uuid = (r.json()[0])['ID']
        
        #Get diocm series zip 
        r = requests.get('http://localhost:8042/series/' + uuid + '/archive')
        with open(seriesId + '.zip','wb') as f:
            f.write(r.content)
        
        #extract zip file
        zf = zipfile.ZipFile(seriesId + '.zip', 'r')
        zf.extractall(seriesId) 
        for root, dirs, files in os.walk("./" + seriesId):       
            for f in files:
                fullpath = join(root, f)
                shutil.move(fullpath, "./" + seriesId)
        
        #renaming diocm file
        rename_SOPInstanceUID.batch_rename("./" + seriesId + "/")
    return seriesId
        
#Id = DicomRequests('1.3.12.2.1107.5.1.4.73158.30000017082121422968200045335')