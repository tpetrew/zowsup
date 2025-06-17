from ...layers import YowProtocolLayer
from .protocolentities import *
from ...layers.protocol_messages.protocolentities.attributes.converter import AttributesConverter
from ...layers.protocol_messages.protocolentities.attributes.attributes_message_meta import MessageMetaAttributes
from ...layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from ...layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity

import logging
logger = logging.getLogger(__name__)


class YowMessagesProtocolLayer(YowProtocolLayer):
    def __init__(self):
        handleMap = {
            "message": (self.recvMessageStanza, self.sendMessageEntity)
        }
        super(YowMessagesProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Messages Layer"

    def sendMessageEntity(self, entity):        
        if entity.getType() in ["text","poll"]:                              
            self.entityToLower(entity)

    ###recieved node handlers handlers    
    def recvMessageStanza(self, node):            

        if node.getAttributeValue("from").endswith("@newsletter"):
            self.toLower(OutgoingReceiptProtocolEntity(
                            messageIds=[node["id"]],
                            to=node["from"],
                            view=True,
                            serverIds=node["server_id"]
                        ).toProtocolTreeNode())    
            return               
         
        protoNode = node.getChild("proto")                                
        if protoNode is None :
            return
        
        if node.getAttributeValue("type")=="reaction":
            #reaction,特殊处理
            converter = AttributesConverter.get()
            proto = converter.protobytes_to_proto(protoNode.getData())                            

            message = converter.proto_to_message(proto,from_jid=node.getAttributeValue("from"))                                  

            self.toUpper(
                ReactionMessageProtocolEntity(
                    message.reaction,
                    MessageMetaAttributes.from_message_protocoltreenode(node,proto)
                )
            )
        
        elif node.getAttributeValue("type")=="poll":

            #投票，特殊处理
            converter = AttributesConverter.get()
            message_db = self.getStack().getProp("profile").axolotl_manager  

            proto = converter.protobytes_to_proto(protoNode.getData())
            message = converter.proto_to_message(proto,from_jid=node.getAttributeValue("from"),message_db=message_db)                                  

            self.toUpper(
                PollUpdateMessageProtocolEntity(
                    message.poll_update,
                    MessageMetaAttributes.from_message_protocoltreenode(node,proto)
                )
            )       
        else:                                 
            if protoNode and protoNode["mediatype"] is None:
                #mediatype的统一在其它层处理，这里忽略
                converter = AttributesConverter.get()
                proto = converter.protobytes_to_proto(protoNode.getData())                            
                message = converter.proto_to_message(proto)                

                if message.conversation:
                    self.toUpper(
                        TextMessageProtocolEntity(
                            message.conversation, 
                            MessageMetaAttributes.from_message_protocoltreenode(node,proto),                            
                        )
                    )
                elif message.extended_text:
                    
                    self.toUpper(
                        ExtendedTextMessageProtocolEntity(
                            message.extended_text,
                            MessageMetaAttributes.from_message_protocoltreenode(node,proto)
                        )
                    )                                                                       
                    
                elif not message.sender_key_distribution_message:
                    # Will send receipts for unsupported message types to prevent stream errors
                    logger.warning("Unsupported message type: %s, will send receipts to "
                                    "prevent stream errors" % message)
                       
                    self.toLower(
                        OutgoingReceiptProtocolEntity(
                            messageIds=[node["id"]],
                            to=node["from"],
                            participant=node["participant"]
                        ).toProtocolTreeNode()
                    )              



