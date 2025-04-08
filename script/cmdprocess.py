# coding=UTF-8
import os,sys
sys.path.append(os.getcwd())
from unicodedata import name
from conf.constants import SysVar
from proto import wsend_pb2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)))

import logging
import threading
import time
import json

logger = logging.getLogger(__name__)

class CmdProcess:

    def __init__(self,bot,args,options,taskId=None,partNo=None):                                
        self.bot = bot            
        self.args = args        
        self.options = options

        self.thread = threading.Thread(target=self.runThread)
        self.thread.setDaemon(True)

    def waitLogin(self):
        return self.bot.waitLogin() 

    def runThread(self):
        logger.info("Waiting BOT %s " % self.bot.botId) 

        if self.waitLogin():       
            if self.bot.sendLayer.detect40x:
                logger.info("BOT %s login failed" % self.bot.botId)    
                self.bot.disconnect()                 
            else:
                logger.info("BOT %s ready，starting command" % self.bot.botId)                
                waitTime = 0                
                if self.args[0]=="init":                
                    waitTime = 10                            
                else:
                    waitTime = 20

                if SysVar.CMD_WAIT is not None:                
                    waitTime = SysVar.CMD_WAIT             
                                
                cmdId,errMsg = self.bot.callDirect(self.args[0],self.args[1:] if  len(self.args)>1 else [],self.options)        

                if errMsg is not None:
                    logger.info("Commmand %s error(execute stage），info=%s" % (self.args[0],errMsg))      
                else:                    
                    if cmdId=="JUSTWAIT":                         
                        logger.info("Command JUSTWAIT %d seconds" % waitTime) 
                        time.sleep(waitTime)
                        logger.info("Command complete") 
                    else:
                        result,errMsg = self.bot.getCmdResult(cmdId,waitTime)                    

                        if errMsg is not None:
                            logger.info("Command %s error (result stage），info=%s" % (self.args[0],errMsg)) 
                    
                        else:
                            logger.info("Command %s complete，result=%s" % (self.args[0],json.dumps(result)))

                                   
                self.bot.disconnect()           

        else:
            logger.info("BOT %s connection timeout" % self.bot.botId)    
            self.bot.disconnect() 
    
    def run(self):       

        self.thread.start()




        

        




        
        
                

