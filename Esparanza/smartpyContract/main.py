import smartpy as sp
FA2 = sp.io.import_script_from_url("https://legacy.smartpy.io/templates/fa2_lib.py")

class NFT(FA2.Fa2Nft):
    @sp.entry_point
    def mint(self, owner, token_info):
        token_id = self.data.last_token_id
        self.data.ledger[token_id]=owner
        self.data.token_metadata[token_id]=sp.record(
            token_id = token_id, token_info=token_info
        )
        self.data.last_token_id +=1
        

    
@sp.add_test(name="NFT")
def test():
    sc=sp.test_scenario()
    nft=NFT(
        metadata= sp.utils.metadata_of_url(
            "ipfs://QmdaJhsduJLwroiKCwGmm7SjB6AGnX9mkMdNcjzkH2rhrS"
        )
    )
    sc +=nft
    abhi = sp.address("tz1d1YftUDiJ7vfDsvFEv3CwfnhGTZD3vYRS")
    rishabh= sp.address("tz1TwWvtgRPmiGZkVBd1VWg7u4MpGFcnhwhh")
    sc.show(sp.record(abhi = abhi, rishabh= rishabh))
    sc.h2("Mint")
    nft.mint(
        owner = abhi,
        token_info = sp.map({
            "":sp.utils.bytes_of_string(
                "ipfs://QmdaJhsduJLwroiKCwGmm7SjB6AGnX9mkMdNcjzkH2rhrS"
            )
        })
    )
    sc.verify(nft.data.ledger[0]== abhi)

    sc.h2("Transfer")
    nft.transfer(
        [
            sp.record(
                from_= abhi,
                txs = [sp.record(to_=rishabh, amount=1, token_id =0)],
            )
        ]
    ).run(sender=abhi)

    sc.verify(nft.data.ledger[0] == rishabh)