from Crypto.Hash import keccak
from eth_abi import encode
from eth_account import Account
from eth_account.messages import encode_defunct


def generate_hash(user_id: int) -> bytes:
    k = keccak.new(digest_bits=256)
    user_id = encode(['uint256'], [user_id])
    k.update(user_id)
    return k.digest()


def generate_signature(user_id: int,
                       private_key: str):
    keccak_hash = generate_hash(user_id)
    message = encode_defunct(keccak_hash)
    account = Account.from_key(private_key)
    signature = account.sign_message(message)
    return signature.signature



