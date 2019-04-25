#!/usr/bin/python3.7
import pexpect,sys,os,datetime


def writeLog(message,logfile):
    with open(logfile, "a") as f:
        f.write(message)


def getSwitchConfig(name,ip,port,username,password,command,filename):
    #拼接登陆后需要执行的指令
    cmd =  'ssh -p ' + str(port) + " " + username + "@" + ip
    logfile = "/var/log/switch-task.log"

    #ssh登录过程处理
    loginPrompt = ['(p|P)assword:','continue connecting (yes/no)?']
    try:
        child = pexpect.spawn(cmd)
        fout = open(filename, 'wb+')
        #child.logfile = fout

        pr = child.expect(loginPrompt)
        if pr == 0:
            child.sendline(password)
        else:
            child.sendline("yes")
            child.expect("password:")
            child.sendline(passwd)

        #记录输出内容
        child.logfile = fout
        child.expect("<%s>"%name)
        #执行给定指令
        child.sendline(command)

        #计数器-防止死循环
        counter = 0
        #分页交互-获取指令的全部输出
        while True:
            counter += 1
            index = child.expect(["---- More ----", "<%s>"%name])
            #print(index)
            if index == 0:
                child.send(" ")
            else:
                child.send("quit")
                print("The task of %s's backup is done ..." % name)
                break
            if counter > 300:
                #记录日志
                message = datetime.datetime.now() + " " + name + command + "run times greater than 300"
                writeLog(message,logfile)
                #退出循环
                break
    except:
        message = str(datetime.datetime.now()) + " " + name + " " + command + " " "task run faild\n"
        writeLog(message,logfile)

if __name__ == "__main__":
    #hostlist
    hostDict = {
            "test-switch-01":["129.115.108.54", 22, "admin", "yourpassword"],
            "test-switch-02":["119.215.3.20", 22, "admin", "yourpassword"],
            "test-switch-03":["139.115.223.50", 22, "admin", "yourpassword"],
            }

    path = r"/home/backup/switch_config/"
    savePath = os.path.join(path,str(datetime.datetime.now().strftime("%Y%m%d")))
    command = 'dis cur'

    os.system("mkdir -p " + savePath)


    
    for k,v in hostDict.items():
        filename = savePath + "/" + k + "_" + datetime.datetime.now().strftime("%Y%m%d") + ".config"
        #print(filename)
        getSwitchConfig(k,v[0],v[1],v[2],v[3],command,filename)
    



