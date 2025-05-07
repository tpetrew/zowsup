class MessageMetaAttributes(object):

    ID_ANDROID = 0
    ID_IOS = 1

    def __init__(
            self, id=None, sender=None, recipient=None, notify=None, timestamp=None, participant=None, offline=None,
            retry=None,fromMe=False,category=None,phash=None,edit=None
    ):
        self.id = id
        self.sender = sender
        self.recipient = recipient
        self.notify = notify        
        self.timestamp = int(timestamp) if timestamp else None
        self.participant = participant
        self.offline = offline in ("1", True)
        self.retry = int(retry) if retry else None
        self.fromMe = fromMe if fromMe else False      
        self.category = category
        self.phash = phash
        self.edit = edit

    @staticmethod
    def from_message_protocoltreenode(node,proto=None):

        fromMe = False
        to = None
        if proto is not None:
            if proto.HasField("device_sent_message"):
                fromMe = True                
                to = proto.device_sent_message.destination_jid
        

        return MessageMetaAttributes(
            node["id"], node["from"], node["to"] if to is None else to, node["notify"], node["t"], node["participant"], node["offline"],
            node["retry"],fromMe,node["category"],node["phash"],node["edit"]
        )
