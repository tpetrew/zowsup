from yowsup.structs import ProtocolTreeNode
from .iq_sync import SyncIqProtocolEntity

class ResultSyncIqProtocolEntity(SyncIqProtocolEntity):
    '''
    <iq type="result" from="491632092557@s.whatsapp.net" id="1417046561-4">
        <usync index="0" wait="166952" last="true" version="1417046548593182" sid="1.30615237617e+17">
            <result>
                <lid/>
                <disappearing_mode />
                <devices />
                <business />
                <status />
                <contact version="1417046548593182"/>    
            </result?
            <list>
                <user jid=".....">
                    <contact type="in/out" />
                        +8618500000000
                    </contact>
                </user>
                <user jid=".....">
                    <contact type="in/out" />
                        +8618500000000
                    </contact>
                </user>
                <user jid=".....">
                    <contact type="in/out" />
                        +8618500000000
                    </contact>
                </user>
            </list>            
        </usync>
    </iq>
    '''

    def __init__(self,_id, sid, index, last, version, inNumbers, outNumbers, wait = None):
        super(ResultSyncIqProtocolEntity, self).__init__("result", _id, sid, index, last)
        self.setResultSyncProps(version, inNumbers, outNumbers, wait)

    def setResultSyncProps(self, version, mode, inNumbers, outNumbers, wait = None):
        assert type(inNumbers) is dict, "in numbers must be a dict {number -> jid}"
        assert type(outNumbers) is dict, "out numbers must be a dict {number -> jid}"

        self.inNumbers = inNumbers
        self.outNumbers = outNumbers
        self.wait = int(wait) if wait is not None else None
        self.version = version
        self.mode = mode

    def __str__(self):
        out  = super(SyncIqProtocolEntity, self).__str__()
        if self.wait is not None:
            out += "Wait: %s\n" % self.wait
        out += "Version: %s\n" % self.version
        out += "In Numbers: %s\n" % (",".join(self.inNumbers))
        out += "Out Numbers: %s\n" % (",".join(self.outNumbers))

        return out

    def toProtocolTreeNode(self):

        users = []

        for number,jid in self.inNumbers.items():
            contact =ProtocolTreeNode("contact",{type:"in"},None,number)
            user = ProtocolTreeNode("user",{jid:jid},None,None)
            user.addChild(contact)
            users.append(user)            

        for number,jid in self.outNumbers.items():
            contact =ProtocolTreeNode("contact",{type:"out"},None,number)
            user = ProtocolTreeNode("user",{jid:jid},None,None)
            user.addChild(contact)
            users.append(user)   

        for number in self.invalidUsers:
            contact =ProtocolTreeNode("contact",{type:"invalid"},None,number)
            user = ProtocolTreeNode("user",{},None,None)
            user.addChild(contact)
            users.append(user)

        node = super(ResultSyncIqProtocolEntity, self).toProtocolTreeNode()
        syncNode = node.getChild("usync")
        syncNode.setAttribute("version", self.version)

        if self.wait is not None:
            syncNode.setAttribute("wait", str(self.wait))

        if len(users):
            syncNode.addChild(ProtocolTreeNode("list", children = users))

        return node

    @staticmethod
    def fromProtocolTreeNode(node):

        syncNode         = node.getChild("usync")
        resultNode       = syncNode.getChild("result")
        listNode         = syncNode.getChild("list")

        mode = syncNode.getAttributeValue("mode")
        
        version = resultNode.getChild("contact").getAttributeValue("version")

        inUsersDict = {}
        outUsersDict = {}     


        users = listNode.getAllChildren() if listNode else []

        for user in users:
            contact = user.getChild("contact")
            type = contact.getAttributeValue("type")
            if type=="in":                                
                inUsersDict[contact.data.decode()] = user.getAttributeValue("jid")                
            elif type=="out":
                outUsersDict[contact.data.decode()] = user.getAttributeValue("jid")                                            
                    
        
        entity           = SyncIqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = ResultSyncIqProtocolEntity

        entity.setResultSyncProps(version,
            mode,
            inUsersDict,
            outUsersDict,
            
            syncNode.getAttributeValue("wait")
        )

        return entity
