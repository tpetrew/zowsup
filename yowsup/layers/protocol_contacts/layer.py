from ...layers import YowProtocolLayer
from .protocolentities import *
import logging

logger = logging.getLogger(__name__)


class YowContactsIqProtocolLayer(YowProtocolLayer):
    def __init__(self):
        handleMap = {
            "iq": (self.recvIq, self.sendIq),
            "notification": (self.recvNotification, None)
        }
        super(YowContactsIqProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Contact Iq Layer"

    def recvNotification(self, node):

        if node["type"] == "contacts":
            if node.getChild("remove"):
                self.toUpper(RemoveContactNotificationProtocolEntity.fromProtocolTreeNode(node))

            elif node.getChild("add"):
                self.toUpper(AddContactNotificationProtocolEntity.fromProtocolTreeNode(node))

            elif node.getChild("update"):
                self.toUpper(UpdateContactNotificationProtocolEntity.fromProtocolTreeNode(node))

            elif node.getChild("usync"):
                self.toUpper(ContactsSyncNotificationProtocolEntity.fromProtocolTreeNode(node))

            else:
                logger.warning("Unsupported contact notification type: %s " % node["type"])
                logger.debug("Unsupported contact notification node: %s" % node)

    def recvIq(self, node):        
        if node["type"] == "result":            
            usyncNode = node.getChild("usync")
            if usyncNode:            
                if usyncNode["context"]=="interactive" or usyncNode["context"]=="registration":
                    entity = ResultSyncIqProtocolEntity.fromProtocolTreeNode(node)            
                    self.toUpper(entity)                

                    
    def sendIq(self, entity):
        if entity.getXmlns() == "usync":
            node = entity.toProtocolTreeNode()            
            self.toLower(node)        
