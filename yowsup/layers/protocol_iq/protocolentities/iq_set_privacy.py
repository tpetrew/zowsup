from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq import IqProtocolEntity
class SetPrivacyIqProtocolEntity(IqProtocolEntity):
    
    def __init__(self, jids,timestamp,_id = None ):
        super(SetPrivacyIqProtocolEntity, self).__init__("privacy" , _id = _id, _type = "set",to="s.whatsapp.net")     
        self.jids = jids 
        self.timestamp = timestamp  

    def toProtocolTreeNode(self):
        node = super(SetPrivacyIqProtocolEntity, self).toProtocolTreeNode()
        tokens = ProtocolTreeNode("tokens",{})
        jidList = self.jids.split(",")

        for jid in jidList:
            token = ProtocolTreeNode("token",{"jid":jid,"type":"trusted_contact","t":str(self.timestamp)})
            tokens.addChild(token)        
                        
        node.addChild(tokens)      
        
        return node    
