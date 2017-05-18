#!/usr/bin/env python
#coding=utf8

# import xlwt
# def createExcel():
#     style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')
#     wb = xlwt.Workbook()
#     ws = wb.add_sheet('A Test Sheet', cell_overwrite_ok=True)
#     return ws

#
#里面路径写死了，为了读取tray每个slot unit的sn, 最后会按slot排序输出sn方便写dry run report
#需要放到tray的Mac Mini上去运行
#

#!/usr/bin/env python
#coding=utf8

import os.path
import fnmatch
import glob
import time
import re

#parser = argparse.ArgumentParser()
#parser.add_argument('-p','--requestParseFilePath', help='Request Parse File Path', required=True)
#parser.add_argument('-n','--newfile', help='New overlay Pivot CSV', required=True)
#parser.add_argument('-r','--resultfile', help="HTML file for result (default './diff_result.html')", default="diff_result.html")
#parser.add_argument('-d','--displayhtml', help='Open the HTML result in a browser.', action="store_true")
#parser.add_argument('-i','--itemsonly',help='Only compare test items, not limits or units.', action="store_true")
    
def recursivelyFindFilesAtPath(dirPath, partInfoName):
    fileList = []
    filesPath = glob.glob(os.path.join(dirPath, '*'))
    #print "fiesPath = %s" %filesPath
    for filePath in filesPath:
        #print "filePath = %s" %filePath
        if os.path.isfile(filePath) and fnmatch.fnmatch(filePath, partInfoName):
            fileList.append(filePath)
        elif os.path.isdir(filePath):
            fileList += recursivelyFindFilesAtPath(filePath, partInfoName)
    return fileList

if __name__ == "__main__":
    startTime = time.time()
    
    #inputPath = raw_input("FilePath: ") //等待输入路径
    #print inputPath 
    #args = parser.parse_args()
    snList = {}
    #print "Waiting Parse Path -->>>> " + args.requestParseFilePath
    #获取需要解析的文件夹的路径(每个sip的测试log里面必定有fixutre log不然肯定没有rawuart.log和smokey.log和testprocess.log)
    #fileListWithFixtureLogs = recursivelyFindFilesAtPath(args.requestParseFilePath, "*fixtureSlot*.log")
    #fileListWithFixtureLogs = recursivelyFindFilesAtPath(inputPath[0:-1]+"/", "*fixtureSlot*.log")//
    fileListWithFixtureLogs = recursivelyFindFilesAtPath('/vault/atlas/Apps/Hyperion/', "*fixtureSlot*.log")

    for oneSIPFilePathWithFixtureLog in fileListWithFixtureLogs:
        print oneSIPFilePathWithFixtureLog
        #/UnknownUnits/Slot-1/20170407_17-10-45/AtlasLogs/fixtureSlot1.log
        #/UnknownUnits/Slot-1/20170407_17-10-45/AtlasLogs/
        oneSIPFilePathWithAtlasLog = "/".join(oneSIPFilePathWithFixtureLog.split("/")[0:-1])
        print oneSIPFilePathWithAtlasLog
        oneSIPFilePathWithAttributesCSV = oneSIPFilePathWithAtlasLog+"/Attributes.csv"
        if os.path.isfile(oneSIPFilePathWithAttributesCSV):
            print "-> Attributes.csv exist"
            try:
                with open(oneSIPFilePathWithAttributesCSV, "r") as f:
                    content = f.read() #读取文件中所有内容，为一个字符串
                   
                    regex = re.compile("(FN.+?)$", re.M)
                    if regex.search(content) != None:
                        print "xyz ===> "+regex.search(content).group(1)
                        sn = regex.search(content).group(1)
                        print "SN = " + sn

                        regexSlot = re.compile("fixtureSlot([0-9]{1}).log$", re.M)
                        print "Slot ===> "+regexSlot.search(oneSIPFilePathWithFixtureLog).group(1)
                        slot = regexSlot.search(oneSIPFilePathWithFixtureLog).group(1)
                        snList[slot] = sn
                        print snList
                    
                    else:
                        print "xyz ===> Can't find keyword from content!"
                    #m = re.search(r'SrNm: (.*)$', content)
                    #print "DIAGSVER = "+ m.group(0)
                    
#             except Exception,e:  
#                 print Exception,":",e        
            except:
                print "GET SN FAIL!"
        else:
            print "No need log existed"

    snListSorted = sorted(snList.iteritems(), key = lambda snList:snList[0], reverse = False)
    print snList
    print snListSorted
    restoreInfoFH = open("/Users/gdlocal/Desktop/Restore Info.txt",'r')
    content = restoreInfoFH.read()
    regex = re.compile("UNIT=X988 SMT-BURNIN #(.+)$", re.M)
    if regex.search(content) != None:
        trayID = regex.search(content).group(1)
        print "TrayID = " + trayID
    else:
        print "xyz ===> Can't find keyword from content!"
    
    snFileListHander = open("/Users/gdlocal/Desktop/Tray"+trayID+".csv",'w')
    for dictSnList in snListSorted:
        snFileListHander.write(dictSnList[1]+'\n')












            