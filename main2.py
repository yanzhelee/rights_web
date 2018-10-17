#encoding=utf-8
from bottle import route, run, request,static_file,template
import pymysql
import json

@route('/main')
def main():
    return static_file("main.html", root='./static/html')

@route('/getItemList')
def getItemList():
    params = request.params
    page = int(params["page"])-1
    db = pymysql.connect("172.16.4.22", "intelligent", "intelligent", "ailab", charset="utf8")
    cursor = db.cursor()

    cursor.execute("select count(1) from new_case")
    results = cursor.fetchone()
    rowcounts = results[0]
    pagenum = rowcounts / 10 + 1
    if (rowcounts % 10 == 0):
        pagenum = pagenum - 1

    cursor.execute("select ID,CASE_NAME from new_case limit "+str(page*10)+",10")
    results = cursor.fetchall()
    list = []
    for row in results:
        item = {}
        item["id"] = row[0]
        item["content"] = row[1]
        list.append(item)
    result = {}
    result["data"]=list
    result["pagenum"]=pagenum
    return json.dumps(result,ensure_ascii=False)

@route('/itemView/<id>')
def itemView(id):
    db = pymysql.connect("172.16.4.22", "intelligent", "intelligent", "ailab", charset="utf8")
    cursor = db.cursor()
    # 查询文章
    cursor.execute("select Id,CASE_NAME,CONTENT,rights from  data_case_rights where id=" + id)
    content = cursor.fetchone()
    file = {}
    file["id"]=content[0]
    file["title"] = content[1]
    file["content"] = content[2]
    file["rights"] = []
    markedRights = content[3].split(',')
    rightStr = ""
    for right in markedRights:
        rightStr += str(right)+","
    if(len(rightStr)>0):
        rightStr = rightStr[:-1]
        cursor.execute("select id,right_no,right_name from rights where id in (" + rightStr +") order by id asc")
        file["rights"] = cursor.fetchall()

    # 查询权利清单
    rights = {}
    cursor.execute("select version,result,version_des from match_rights where caseId ="+id +" order by version asc")
    results = cursor.fetchall()
    for row in results:
        item = {}
        item["version"] = str(row[0])+"("+row[2]+")"
        #解析权利清单
        rightList = json.loads(row[1].replace("'", "\""))
        rightStr = ""
        for right in rightList:
            rightStr += str(right["uniqueId"]) + ","
        if (len(rightStr) > 0):
            rightStr = rightStr[:-1]
            cursor.execute("select id,right_no,right_name from rights where id in (" + rightStr + ") order by id asc")
            rightListTemp = cursor.fetchall()
            item["rights"] = []
            #设置权限
            for right1 in rightListTemp:
                for right2 in rightList:
                    if(right1[0] == int(right2["uniqueId"])):
                        try:
                            weight = right2["weight"]
                        except:
                            weight = right2["distance"]
                        index = 0
                        for pos in range(len(item["rights"])):
                            if(item["rights"][pos][3]>weight):
                                index = pos+1
                        right1 = right1 + (weight,)
                        item["rights"].insert(index,list(right1))
                        break

        #if (rights.has_key(item["version"]) == False):
        if (rights.get(item["version"]) is None):
            rights[item["version"]] = []
        rights[item["version"]]=item
    result = {}
    result["content"] = file
    result["rights"] = rights
    return template('itemView', data=json.dumps(result,ensure_ascii=False))

@route('/static/css/<filename>')
def server_static(filename):
    return static_file(filename, root='./static/css')

@route('/static/js/<filename>')
def server_static(filename):
    return static_file(filename, root='./static/js')

run(host='0.0.0.0', port=8080, debug=True)