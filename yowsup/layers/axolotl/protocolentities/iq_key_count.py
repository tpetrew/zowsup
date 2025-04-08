from yowsup.common import YowConstants
from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
from yowsup.structs import ProtocolTreeNode


class GetKeysCountIqProtocolEntity(IqProtocolEntity):
    def __init__(self):
        super(GetKeysCountIqProtocolEntity, self).__init__("encrypt", _type="get", to=YowConstants.WHATSAPP_SERVER)

    def toProtocolTreeNode(self):
        node = super(GetKeysCountIqProtocolEntity, self).toProtocolTreeNode()
        countNode = ProtocolTreeNode("count")
        node.addChild(countNode)
        return node
