from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .notification import NotificationProtocolEntity

class LinkCodeCompanionRegNotificationProtocolEntity(NotificationProtocolEntity):
    '''        

        stawge = companion_hello

        <notification from="s.whatsapp.net" type="link_code_companion_reg" id="845463461" offline="0" t="1723164552">
            <link_code_companion_reg stage="companion_hello" should_show_push_notification="false">
                <link_code_pairing_wrapped_companion_ephemeral_pub>
                0x240afffb336a1debad83fbf4ec29aa7d144984f8f34887957f94febd4424aa12b6f88bdf9d98f240f783f3209db51cf11a3874cb4db33de623157b21f4ca73b2c3d57df4217d34fd56a3210bb300ea51
                </link_code_pairing_wrapped_companion_ephemeral_pub>
                <link_code_pairing_nonce>
                0x00
                </link_code_pairing_nonce>
                <companion_server_auth_key_pub>
                0x7fe3e82327686d6704fe463551db26c61973b9696d864974ee85e1102a65cf2d
                </companion_server_auth_key_pub>
                <companion_platform_id>
                0x31
                </companion_platform_id>
                <companion_platform_display>
                0x4368726f6d6520284d6163204f5329
                </companion_platform_display>
                <link_code_pairing_ref>
                0x3340323a6d32317256794d44234b2b4352474553775370346f75363361575a68644b4d69544a5473452b3067744b6836747234716d31755166364641704c79644c46695348394e4f6e4f73687877364f635856787279476a586d673d3d
                </link_code_pairing_ref>
            </link_code_companion_reg>
        </notification>


        stage = companion_finish

        <notification from="s.whatsapp.net" type="link_code_companion_reg" id="2330712893" t="1723190864">
            <link_code_companion_reg stage="companion_finish">
                <link_code_pairing_wrapped_key_bundle>
                0x452c1034bf6d4857d77a22ec4bfa5d39d8c011b7ad10d2b691644e3390ed9de7f228bf26a6c577e65f74ba8ae1c00c8d07db231a0de303a5575c00c30c1d25db6534785fda6447878f78bdfacb6c1078abf7f7a2b3a97ac95217d518ae3f8bebdfa2d78aed4c315a007150847ee1d1b4a053314e4753fb08c50a06f0a950e2794718b5ae6d5e559fec6ac1536c1d1f604cd754a33d0e925897669316
                </link_code_pairing_wrapped_key_bundle>
                <companion_identity_public>
                0xa5c0fdecff058542a6f19c67fb64680585c7b482de973c95dcde5382b68edc13
                </companion_identity_public>
                <link_code_pairing_ref>
                0x3340323a6d32317256794d44236a74303749384c2f64314f416a6d5858303955654d58663768304935414645723964725a785236576479424a6630504e5933464969776f786c2b546f414d70484b2b3134684765444f772b64387865357766665834387975777651316564765a6a6a4d3d
                </link_code_pairing_ref>
            </link_code_companion_reg>
        </notification>        
    '''

    def __init__(self, _id,  _from, stage, timestamp, notify, offline):
        super(LinkCodeCompanionRegNotificationProtocolEntity, self).__init__(_id, _from, timestamp, notify, offline)
        self.stage = stage

        #for hello
        self.linkCodePairingWrappedCompanionEphemeralPub = None
        self.linkCodePairingNonce = None
        self.companionServerAuthKeyPub = None
        self.companionPlatformId = None
        self.companionPlatformDisplay = None
        
        #for finish
        self.linkCodePairingWrappedKeyBundle = None
        self.companionIdentityPublic = None

        #for both
        self.linkCodePairingRef = None


    @staticmethod
    def fromProtocolTreeNode(node):
        entity = NotificationProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = LinkCodeCompanionRegNotificationProtocolEntity
        node = node.getChild("link_code_companion_reg")
        entity.stage = node.getAttributeValue("stage")

        #for hello
        entity.linkCodePairingWrappedCompanionEphemeralPub = node.getChild("link_code_pairing_wrapped_companion_ephemeral_pub").getData() if node.getChild("link_code_pairing_wrapped_companion_ephemeral_pub") is not None else None
        entity.linkCodePairingNonce = node.getChild("link_code_pairing_nonce").getData() if node.getChild("link_code_pairing_nonce") is not None else None
        entity.companionServerAuthKeyPub = node.getChild("companion_server_auth_key_pub").getData() if node.getChild("companion_server_auth_key_pub") is not None else None
        entity.companionPlatformId = node.getChild("companion_platform_id").getData() if node.getChild("companion_platform_id") is not None else None
        entity.companionPlatformDisplay = node.getChild("companion_platform_display").getData() if node.getChild("companion_platform_display") is not None else None

        #for finish
        entity.linkCodePairingWrappedKeyBundle = node.getChild("link_code_pairing_wrapped_key_bundle").getData() if node.getChild("link_code_pairing_wrapped_key_bundle") is not None else None
        entity.companionIdentityPublic = node.getChild("companion_identity_public").getData() if node.getChild("companion_identity_public") is not None else None

        #for both
        entity.linkCodePairingRef = node.getChild("link_code_pairing_ref").getData() if node.getChild("link_code_pairing_ref") is not None else None


        return entity