smartctl = './Mine/smart/here/' # smartctl 경로

exe = './smartctl.exe'

scan = '--scan'

# 뒤에 scan한 path 필요

help = '-h'
attrb = '-A'
info = '-i'    # try로




import subprocess
from subprocess import Popen, PIPE
import shlex

import os
# pathnow = (os.getcwd())   # 현재 작업 경로 알기3
# print(pathnow)
# os.chdir(smartctl)  # 작업 경로 변경

path = os.chdir(smartctl)

# print (os.getcwd())

def cmd(x, n, *args):
    if n == 2: 
        output = subprocess.check_output(shlex.split('{} {}'.format(*args)))
    elif n == 3:
        output = subprocess.check_output(shlex.split('{} {} {}'.format(*args)))
    data = output.decode('cp949')
    
    
    if x == 1:  # info  // dict
        
        lines = data.split('Device Model:')[1]
        lines = lines.split('\n')[0]
        name = lines.replace(' ','')
        
        
        lines = data.split('Serial Number:')[1]
        lines = lines.split('\n')[0]
        serial = lines.replace(' ','')
        
        lines = [name, serial]
        
        
        return lines
    
    elif x == 2:
        lines = data.split('ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE')[1]
        lines = lines.splitlines()
        
        # 필요한 값만 빼내기
        
        
        return lines
        
    lines = data.splitlines()
    
    return lines


scanL = cmd(0, 2, exe, scan)

# print(lines)

diskpath = [] # smartctl -> disk path
for i in range(0, len(scanL)):
    try:
        x = scanL[i].split(' #')
        diskpath.append(x[0])
    except:
        pass
    
    
# print(diskpath)

infoLI = []
letsgo = 0
for i in range(0, len(scanL)):
    
    try:
        # Serial Num
        infoL = cmd(1, 3, exe, info,  diskpath[i])

        print('Disk Name : ', infoL[0])
        print('Serial Num : ', infoL[1])
        infoLI.append(infoL)
    except:
        pass
    
    if len(infoLI) > 1: # 시리얼 값이 같면 패스
        if infoLI[i-1] in infoLI and len(list(filter(lambda x: infoLI[i-1] == infoLI[x], range(len(infoLI))))) > 1:
            letsgo += 1    
    
    if letsgo == 0: # 만약에 raw값이 이상하게도 같을 경우엔 pass?
        attrbL = cmd(2, 3, exe, attrb,  diskpath[i])    # 리스트 개별 하나당 앞에 3까지 끊으면 숫자 구별 가능

        print(attrbL)
        



    # print('>>>>>>>>>>>>>>>>>>>')


# SMART 값은 DISK 마다 다를 수 있을 수 있으니, 
