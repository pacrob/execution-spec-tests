"""_summary_
test `CALLDATACOPY` opcode
"""

import pytest

from ethereum_test_tools import (
    Account,
    Alloc,
    Bytecode,
    Environment,
    Hash,
    StateTestFiller,
    Transaction,
)
from ethereum_test_tools.vm.opcode import Opcodes as Op

local_pre = {
    0x0000000000000000000000000000000000001000: Account(
        balance=0x0BA1A9CE0BA1A9CE,
        # Copy data from calldata locations [1:(1+2)-1] to memory
        # locations [0:(0+2)-1]. So we skip the 0'th byte (the 0x12),
        # and write the second and third bytes into memory locations zero
        # and one.
        #
        # When put into a 256 bit storage cell, this gives us 0x3456....0
        # {
        #     (calldatacopy 0 1 2)
        #     [[0]] @0
        #     (return 0 (msize))
        # }
        code=(
            Op.PUSH1[0x2]
            + Op.PUSH1[0x1]
            + Op.PUSH1[0x0]
            + Op.CALLDATACOPY
            + Op.PUSH1[0x0]
            + Op.MLOAD
            + Op.PUSH1[0x0]
            + Op.SSTORE
            + Op.MSIZE
            + Op.PUSH1[0x0]
            + Op.RETURN
            + Op.STOP
        ),
        nonce=0,
        storage={},
    ),
    # Same as 0x100, but with a length of one
    0x0000000000000000000000000000000000001001: Account(
        balance=0x0BA1A9CE0BA1A9CE,
        # {
        #     (calldatacopy 0 1 1)
        #     [[0]] @0
        #     (return 0 (msize))
        # }
        code=(
            Op.PUSH1[0x1]
            + Op.PUSH1[0x1]
            + Op.PUSH1[0x0]
            + Op.CALLDATACOPY
            + Op.PUSH1[0x0]
            + Op.MLOAD
            + Op.PUSH1[0x0]
            + Op.SSTORE
            + Op.MSIZE
            + Op.PUSH1[0x0]
            + Op.RETURN
            + Op.STOP
        ),
        nonce=0,
        storage={},
    ),
    # Same as 0x100, but with a length of zero
    0x0000000000000000000000000000000000001002: Account(
        balance=0x0BA1A9CE0BA1A9CE,
        # {
        #     (calldatacopy 0 1 0)
        #     [[0]] @0
        #     (return 0 (msize))
        # }
        code=(
            Op.PUSH1[0x0]
            + Op.PUSH1[0x1]
            + Op.PUSH1[0x0]
            + Op.CALLDATACOPY
            + Op.PUSH1[0x0]
            + Op.MLOAD
            + Op.PUSH1[0x0]
            + Op.SSTORE
            + Op.MSIZE
            + Op.PUSH1[0x0]
            + Op.RETURN
            + Op.STOP
        ),
        nonce=0,
        storage={},
    ),
    # ZeroMemExpansion
    0x0000000000000000000000000000000000001003: Account(
        balance=0x0BA1A9CE0BA1A9CE,
        # {
        #     (calldatacopy 0 0 0)
        #     [[0]] @0
        #     (return 0 (msize))
        # }
        code=(
            Op.PUSH1[0x0]
            + Op.PUSH1[0x0]
            + Op.PUSH1[0x0]
            + Op.CALLDATACOPY
            + Op.PUSH1[0x0]
            + Op.MLOAD
            + Op.PUSH1[0x0]
            + Op.SSTORE
            + Op.MSIZE
            + Op.PUSH1[0x0]
            + Op.RETURN
            + Op.STOP
        ),
        nonce=0,
        storage={},
    ),
    # DataIndexTooHigh
    0x0000000000000000000000000000000000001004: Account(
        balance=0x0BA1A9CE0BA1A9CE,
        # {
        #     (calldatacopy 0
        #        0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa 0xff)
        #     [[0]] @0
        #     (return 0 (msize))
        # }
        code=(
            Op.PUSH1[0xFF]
            + Op.PUSH32[0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFA]
            + Op.PUSH1[0x0]
            + Op.CALLDATACOPY
            + Op.PUSH1[0x0]
            + Op.MLOAD
            + Op.PUSH1[0x0]
            + Op.SSTORE
            + Op.MSIZE
            + Op.PUSH1[0x0]
            + Op.RETURN
            + Op.STOP
        ),
        nonce=0,
        storage={},
    ),
    # DataIndexTooHigh 2
    0x0000000000000000000000000000000000001005: Account(
        balance=0x0BA1A9CE0BA1A9CE,
        # {
        #   (calldatacopy 0
        #      0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa 0x09)
        #   [[0]] @0
        #   (return 0 (msize))
        # }
        code=(
            Op.PUSH1[0x9]
            + Op.PUSH32[0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFA]
            + Op.PUSH1[0x0]
            + Op.CALLDATACOPY
            + Op.PUSH1[0x0]
            + Op.MLOAD
            + Op.PUSH1[0x0]
            + Op.SSTORE
            + Op.MSIZE
            + Op.PUSH1[0x0]
            + Op.RETURN
            + Op.STOP
        ),
        nonce=0,
        storage={},
    ),
    # Underflow
    0x0000000000000000000000000000000000001010: Account(
        balance=0x0BA1A9CE0BA1A9CE,
        #
        #  0 PUSH1 1
        #  2 PUSH1 1
        #  4 SSTORE (to have a value that will appear unless we revert)
        #  5 PUSH1 1
        #  7 PUSH1 2
        #  9 CALLDATACOPY
        code=(
            Op.PUSH1[0x1]
            + Op.PUSH1[0x1]
            + Op.SSTORE
            + Op.PUSH1[0x1]
            + Op.PUSH1[0x2]
            + Op.CALLDATACOPY
        ),
        nonce=0,
        storage={},
    ),
    # sec, provided as bytecode, disassembled by https://etherscan.io/opcode-tool
    0x0000000000000000000000000000000000001011: Account(
        balance=0x0BA1A9CE0BA1A9CE,
        #  [1] PUSH1 0x05
        #  [2] JUMP                Jump to 5
        #  [3] JUMPDEST            If we got here, failure
        #  [4] STOP
        #  [5] JUMPDEST
        #  [7] PUSH1 0x42
        #  [9] PUSH1 0x1f
        # [10] MSTORE8             mem[0x1f] = 0x42
        # [13] PUSH2 0x0103
        # [15] PUSH1 0x00
        # [17] PUSH1 0x1f
        # [18] CALLDATACOPY        calldatacopy of 0x0103 bytes to memory 0x1f (and later)
        # [20] PUSH1 0x00
        # [21] MLOAD               ; Should be zero
        # [22] DUP1
        # [24] PUSH1 0x60
        # [25] EQ                  ; Is zero equal to 0x60?
        # [27] PUSH1 0x03          ; If so, fail
        # [28] JUMPI
        # [34] PUSH5 0x0badc0ffee      If we got here, success
        # [36] PUSH1 0xff
        # [37] SSTORE
        code=(
            Op.PUSH1[0x5]
            + Op.JUMP
            + Op.JUMPDEST
            + Op.STOP
            + Op.JUMPDEST
            + Op.PUSH1[0x42]
            + Op.PUSH1[0x1F]
            + Op.MSTORE8
            + Op.PUSH2[0x103]
            + Op.PUSH1[0x0]
            + Op.PUSH1[0x1F]
            + Op.CALLDATACOPY
            + Op.PUSH1[0x0]
            + Op.MLOAD
            + Op.DUP1
            + Op.PUSH1[0x60]
            + Op.EQ
            + Op.PUSH1[0x3]
            + Op.JUMPI
            + Op.PUSH5[0xBADC0FFEE]
            + Op.PUSH1[0xFF]
            + Op.SSTORE
        ),
        nonce=0,
        storage={},
    ),
    0xA94F5374FCE5EDBC8E2A8697C15331677E6EBF0B: Account(
        balance=0x0BA1A9CE0BA1A9CE,
        code=b'',
        nonce=0,
        storage={},
    ),
    0xCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC: Account(
        balance=0x0BA1A9CE0BA1A9CE,
        # {
        #     ; Put a 0x10 byte long value in zero (each byte is two hex digits)
        #     ; Then call a contract with just that data. In evm the most
        #     ; significant byte comes first, so the value ends up in memory
        #     ; locations 0x10-0x1F
        #     [0] 0x1234567890abcdef01234567890abcdef0
        #     (call 0xffffff (+ 0x1000 $4) 0
        #        0x0F 0x10   ; arg offset and length to get the 0x1234...f0 value
        #        0x20 0x40)  ; return offset and length
        #     ; Preserve the return data
        #     [[0]] @0x20
        #     [[1]] @0x40
        # }
        code=(
            Op.PUSH17[0x1234567890ABCDEF01234567890ABCDEF0]
            + Op.PUSH1[0x0]
            + Op.MSTORE
            + Op.PUSH1[0x40]
            + Op.PUSH1[0x20]
            + Op.PUSH1[0x10]
            + Op.PUSH1[0xF]
            + Op.PUSH1[0x0]
            + Op.PUSH1[0x4]
            + Op.CALLDATALOAD
            + Op.PUSH2[0x1000]
            + Op.ADD
            + Op.PUSH3[0xFFFFFF]
            + Op.CALL
            + Op.POP
            + Op.PUSH1[0x20]
            + Op.MLOAD
            + Op.PUSH1[0x0]
            + Op.SSTORE
            + Op.PUSH1[0x40]
            + Op.MLOAD
            + Op.PUSH1[0x1]
            + Op.SSTORE
            + Op.STOP
        ),
        nonce=0,
        storage={},
    ),
}
# local_post = {
#     "0x0000000000000000000000000000000000001000": Account(
#         balance=0x0BA1A9CE0BA1A9CE,
#         code="0x60026001600037600051600055596000f300",
#         nonce=0x00,
#         storage={0x00: 0x3456000000000000000000000000000000000000000000000000000000000000},
#     ),
#     "0x0000000000000000000000000000000000001001": Account(
#         balance=0x0BA1A9CE0BA1A9CE,
#         code="0x60016001600037600051600055596000f300",
#         nonce=0x00,
#         storage={},
#     ),
#     "0x0000000000000000000000000000000000001002": Account(
#         balance=0x0BA1A9CE0BA1A9CE,
#         code="0x60006001600037600051600055596000f300",
#         nonce=0x00,
#         storage={},
#     ),
#     "0x0000000000000000000000000000000000001003": Account(
#         balance=0x0BA1A9CE0BA1A9CE,
#         code="0x60006000600037600051600055596000f300",
#         nonce=0x00,
#         storage={},
#     ),
#     "0x0000000000000000000000000000000000001004": Account(
#         balance=0x0BA1A9CE0BA1A9CE,
#         code="0x60ff7ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa600037600051600055596000f300",
#         nonce=0x00,
#         storage={},
#     ),
#     "0x0000000000000000000000000000000000001005": Account(
#         balance=0x0BA1A9CE0BA1A9CE,
#         code="0x60097ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa600037600051600055596000f300",
#         nonce=0x00,
#         storage={},
#     ),
#     "0x0000000000000000000000000000000000001010": Account(
#         balance=0x0BA1A9CE0BA1A9CE,
#         code="0x60016001556001600237",
#         nonce=0x00,
#         storage={},
#     ),
#     "0x0000000000000000000000000000000000001011": Account(
#         balance=0x0BA1A9CE0BA1A9CE,
#         code="0x6005565b005b6042601f536101036000601f3760005180606014600357640badc0ffee60ff55",
#         nonce=0x00,
#         storage={},
#     ),
#     "0x000f3df6d732807ef1319fb7b8bb8522d0beac02": Account(
#         balance=0x00,
#         code="0x3373fffffffffffffffffffffffffffffffffffffffe14604d57602036146024575f5ffd5b5f35801560495762001fff810690815414603c575f5ffd5b62001fff01545f5260205ff35b5f5ffd5b62001fff42064281555f359062001fff015500",
#         nonce=0x01,
#         storage={0x03E8: 0x03E8},
#     ),
#     "0xa94f5374fce5edbc8e2a8697c15331677e6ebf0b": Account(
#         balance=0x0BA1A9CE0B96F005,
#         code="0x",
#         nonce=0x01,
#         storage={},
#     ),
#     "0xcccccccccccccccccccccccccccccccccccccccc": Account(
#         balance=0x0BA1A9CE0BA1A9CF,
#         code="0x701234567890abcdef01234567890abcdef0600052604060206010600f60006004356110000162fffffff15060205160005560405160015500",
#         nonce=0x00,
#         storage={0x00: 0x3456000000000000000000000000000000000000000000000000000000000000},
#     ),
# }

local_post = {
    "0x0000000000000000000000000000000000001000": Account(
        storage={0x00: 0x3456000000000000000000000000000000000000000000000000000000000000},
    ),
    "0x0000000000000000000000000000000000001001": Account(
        storage={},
    ),
    "0x0000000000000000000000000000000000001002": Account(
        storage={},
    ),
    "0x0000000000000000000000000000000000001003": Account(
        storage={},
    ),
    "0x0000000000000000000000000000000000001004": Account(
        storage={},
    ),
    "0x0000000000000000000000000000000000001005": Account(
        storage={},
    ),
    "0x0000000000000000000000000000000000001010": Account(
        storage={},
    ),
    "0x0000000000000000000000000000000000001011": Account(
        storage={},
    ),
    "0x000f3df6d732807ef1319fb7b8bb8522d0beac02": Account(
        storage={0x03E8: 0x03E8},
    ),
    "0xa94f5374fce5edbc8e2a8697c15331677e6ebf0b": Account(
        storage={},
    ),
    "0xcccccccccccccccccccccccccccccccccccccccc": Account(
        storage={0x00: 0x3456000000000000000000000000000000000000000000000000000000000000},
    ),
}


@pytest.mark.parametrize(
    "cdc,tx_data,post",
    [
        (
            (
                Op.PUSH1[0x2]
                + Op.PUSH1[0x1]
                + Op.PUSH1[0x0]
                + Op.CALLDATACOPY
                + Op.PUSH1[0x0]
                + Op.MLOAD
                + Op.PUSH1[0x0]
                + Op.SSTORE
                + Op.MSIZE
                + Op.PUSH1[0x0]
                + Op.RETURN
                + Op.STOP
            ),
            # b"\x00",
            b"i<a9\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
            {
                "0x0000000000000000000000000000000000001000": Account(
                    storage={
                        0x00: 0x3456000000000000000000000000000000000000000000000000000000000000
                    },
                ),
                "0xcccccccccccccccccccccccccccccccccccccccc": Account(
                    storage={
                        0x00: 0x3456000000000000000000000000000000000000000000000000000000000000
                    },
                ),
            },
        ),
        (
            (
                Op.PUSH1[0x1]
                + Op.PUSH1[0x1]
                + Op.PUSH1[0x0]
                + Op.CALLDATACOPY
                + Op.PUSH1[0x0]
                + Op.MLOAD
                + Op.PUSH1[0x0]
                + Op.SSTORE
                + Op.MSIZE
                + Op.PUSH1[0x0]
                + Op.RETURN
                + Op.STOP
            ),
            b"\x01",
            {
                "0x0000000000000000000000000000000000001001": Account(
                    storage={
                        0x00: 0x3400000000000000000000000000000000000000000000000000000000000000
                    },
                ),
                "0xcccccccccccccccccccccccccccccccccccccccc": Account(
                    storage={
                        0x00: 0x3400000000000000000000000000000000000000000000000000000000000000
                    },
                ),
            },
        ),
        (
            (
                Op.PUSH1[0x0]
                + Op.PUSH1[0x1]
                + Op.PUSH1[0x0]
                + Op.CALLDATACOPY
                + Op.PUSH1[0x0]
                + Op.MLOAD
                + Op.PUSH1[0x0]
                + Op.SSTORE
                + Op.MSIZE
                + Op.PUSH1[0x0]
                + Op.RETURN
                + Op.STOP
            ),
            b"\x02",
            {
                "0x0000000000000000000000000000000000001002": Account(
                    storage={0x00: 0x00},
                ),
                "0xcccccccccccccccccccccccccccccccccccccccc": Account(
                    storage={0x00: 0x00},
                ),
            },
        ),
        (
            (
                Op.PUSH1[0x0]
                + Op.PUSH1[0x0]
                + Op.PUSH1[0x0]
                + Op.CALLDATACOPY
                + Op.PUSH1[0x0]
                + Op.MLOAD
                + Op.PUSH1[0x0]
                + Op.SSTORE
                + Op.MSIZE
                + Op.PUSH1[0x0]
                + Op.RETURN
                + Op.STOP
            ),
            b"\x03",
            {
                "0x0000000000000000000000000000000000001003": Account(
                    storage={0x00: 0x00},
                ),
                "0xcccccccccccccccccccccccccccccccccccccccc": Account(
                    storage={0x00: 0x00},
                ),
            },
        ),
        (
            (
                Op.PUSH1[0xFF]
                + Op.PUSH32[0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFA]
                + Op.PUSH1[0x0]
                + Op.CALLDATACOPY
                + Op.PUSH1[0x0]
                + Op.MLOAD
                + Op.PUSH1[0x0]
                + Op.SSTORE
                + Op.MSIZE
                + Op.PUSH1[0x0]
                + Op.RETURN
                + Op.STOP
            ),
            b"\x04",
            {
                "0x0000000000000000000000000000000000001004": Account(
                    storage={0x00: 0x00},
                ),
                "0xcccccccccccccccccccccccccccccccccccccccc": Account(
                    storage={0x00: 0x00},
                ),
            },
        ),
        (
            (
                Op.PUSH1[0x9]
                + Op.PUSH32[0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFA]
                + Op.PUSH1[0x0]
                + Op.CALLDATACOPY
                + Op.PUSH1[0x0]
                + Op.MLOAD
                + Op.PUSH1[0x0]
                + Op.SSTORE
                + Op.MSIZE
                + Op.PUSH1[0x0]
                + Op.RETURN
                + Op.STOP
            ),
            b"\x05",
            {
                "0x0000000000000000000000000000000000001005": Account(
                    storage={0x00: 0x00},
                ),
                "0xcccccccccccccccccccccccccccccccccccccccc": Account(
                    storage={0x00: 0x00},
                ),
            },
        ),
        (
            (
                Op.PUSH1[0x1]
                + Op.PUSH1[0x1]
                + Op.SSTORE
                + Op.PUSH1[0x1]
                + Op.PUSH1[0x2]
                + Op.CALLDATACOPY
            ),
            b"\x10",
            {
                "0x0000000000000000000000000000000000001010": Account(
                    storage={0x01: 0x00},
                ),
            },
        ),
        (
            (
                Op.PUSH1[0x5]
                + Op.JUMP
                + Op.JUMPDEST
                + Op.STOP
                + Op.JUMPDEST
                + Op.PUSH1[0x42]
                + Op.PUSH1[0x1F]
                + Op.MSTORE8
                + Op.PUSH2[0x103]
                + Op.PUSH1[0x0]
                + Op.PUSH1[0x1F]
                + Op.CALLDATACOPY
                + Op.PUSH1[0x0]
                + Op.MLOAD
                + Op.DUP1
                + Op.PUSH1[0x60]
                + Op.EQ
                + Op.PUSH1[0x3]
                + Op.JUMPI
                + Op.PUSH5[0xBADC0FFEE]
                + Op.PUSH1[0xFF]
                + Op.SSTORE
            ),
            b"\x11",
            {
                "0x0000000000000000000000000000000000001011": Account(
                    storage={0xFF: 0xBADC0FFEE},
                ),
            },
        ),
    ],
    ids=[
        "cdc 0 1 2",
        "cdc 0 1 1",
        "cdc 0 1 0",
        "cdc 0 0 0",
        "cdc 0 neg6 ff",
        "cdc 0 neg6 9",
        "underflow",
        "sec",
    ],
)
def test_calldatacopy(
    state_test: StateTestFiller,
    cdc: Bytecode,
    tx_data: bytes,
    # pre: Alloc,
    post: dict,
):

    env = Environment(
        base_fee_per_gas=0xA,
        difficulty=0x20000,
        excess_blob_gas=0x0,
        gas_limit=0x05F55E100,
        prev_randao=0x0,
    )

    # env = Environment()
    pre = Alloc(local_pre)
    sender = pre.fund_eoa() # this is the account that matches the secret key below

    account = pre.deploy_contract(cdc)
    # post = local_post
    # breakpoint()

    tx = Transaction(
        data=tx_data,
        gas_limit=0x04C4B400,
        gas_price=0x0A,
        nonce=0x00,
        secret_key="0x45a915e4d060149eb4365960e6a7a45f334393093061116b197e3240065ff2d8",
        # sender=0xA94F5374FCE5EDBC8E2A8697C15331677E6EBF0B,
        sender=sender,
        to=account,
        value=0x01,
    )

    state_test(env=env, pre=pre, post=post, tx=tx)
