"""_summary_
test `CALLDATACOPY` opcode
"""

import pytest

from ethereum_test_tools import Account, Alloc, Environment, StateTestFiller, Transaction, Yul
from ethereum_test_tools.vm.opcode import Opcodes as Op


local_pre = {
    0x0000000000000000000000000000000000001000: Account(
        balance=0x0ba1a9ce0ba1a9ce,
        code=Yul(
        # Copy data from calldata locations [1:(1+2)-1] to memory
        # locations [0:(0+2)-1]. So we skip the 0'th byte (the 0x12),
        # and write the second and third bytes into memory locations zero
        # and one.
        #
        # When put into a 256 bit storage cell, this gives us 0x3456....0
        """
        {
            (calldatacopy 0 1 2)
            [[0]] @0

            (return 0 (msize))
        }
        """
        ),
        nonce=0,
        storage={},
    ),
    # Same as 0x100, but with a length of one
    0x0000000000000000000000000000000000001001: Account(
        balance=0x0ba1a9ce0ba1a9ce,
        code=Yul(
        """
        {
            (calldatacopy 0 1 1)
            [[0]] @0

            (return 0 (msize))
        }
        """
        ),
        nonce=0,
        storage={},
    ),
    # Same as 0x100, but with a length of zero
    0x0000000000000000000000000000000000001002: Account(
        balance=0x0ba1a9ce0ba1a9ce,
        code=Yul(
        """
        {
            (calldatacopy 0 1 0)
            [[0]] @0

            (return 0 (msize))
        }
        """
        ),
        nonce=0,
        storage={},
    ),
    # ZeroMemExpansion
    0x0000000000000000000000000000000000001003: Account(
        balance=0x0ba1a9ce0ba1a9ce,
        code=Yul(
        """
        {
            (calldatacopy 0 0 0)
            [[0]] @0

            (return 0 (msize))
        }
        """
        ),
        nonce=0,
        storage={},
    ),
    # DataIndexTooHigh
    0x0000000000000000000000000000000000001004: Account(
        balance=0x0ba1a9ce0ba1a9ce,
        code=Yul(
        """
        {
            (calldatacopy 0
               0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa 0xff)
            [[0]] @0

            (return 0 (msize))
        }
        """
        ),
        nonce=0,
        storage={},
    ),



    # DataIndexTooHigh 2
    0000000000000000000000000000000000001005:
      balance: '0x0ba1a9ce0ba1a9ce'
      code: |
        {
          (calldatacopy 0
             0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa 0x09)
          [[0]] @0

          (return 0 (msize))
        }
      nonce: '0'
      storage: {}




    # Underflow
    0000000000000000000000000000000000001010:
      balance: '0x0ba1a9ce0ba1a9ce'
      #
      #  0 PUSH1 1
      #  2 PUSH1 1
      #  4 SSTORE (to have a value that will appear unless we revert)
      #  5 PUSH1 1
      #  7 PUSH1 2
      #  9 CALLDATACOPY
      code: :raw 0x60016001556001600237
      nonce: '0'
      storage: {}


    # sec, provided as bytecode, disassembled by https://etherscan.io/opcode-tool
    0000000000000000000000000000000000001011:
      balance: '0x0ba1a9ce0ba1a9ce'
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
      code: :raw 0x6005565b005b6042601f536101036000601f3760005180606014600357640badc0ffee60ff55
      nonce: '0'
      storage: {}






    cccccccccccccccccccccccccccccccccccccccc:
      balance: '0x0ba1a9ce0ba1a9ce'
      code: |
        {
            ; Put a 0x10 byte long value in zero (each byte is two hex digits)
            ; Then call a contract with just that data. In evm the most
            ; significant byte comes first, so the value ends up in memory
            ; locations 0x10-0x1F

            [0] 0x1234567890abcdef01234567890abcdef0

            (call 0xffffff (+ 0x1000 $4) 0
               0x0F 0x10   ; arg offset and length to get the 0x1234...f0 value
               0x20 0x40)  ; return offset and length

            ; Preserve the return data
            [[0]] @0x20
            [[1]] @0x40
        }
      nonce: '0'
      storage: {}
}
local_post = {
    "0x0000000000000000000000000000000000001000": Account(
        balance=0x0ba1a9ce0ba1a9ce,
        code="0x60026001600037600051600055596000f300",
        nonce=0x00,
        storage={0x00: 0x3456000000000000000000000000000000000000000000000000000000000000},
    ),
    "0x0000000000000000000000000000000000001001": Account(
        balance=0x0ba1a9ce0ba1a9ce,
        code="0x60016001600037600051600055596000f300",
        nonce=0x00,
        storage={},
    ),
    "0x0000000000000000000000000000000000001002": Account(
        balance=0x0ba1a9ce0ba1a9ce,
        code="0x60006001600037600051600055596000f300",
        nonce=0x00,
        storage={},
    ),
    "0x0000000000000000000000000000000000001003": Account(
        balance=0x0ba1a9ce0ba1a9ce,
        code="0x60006000600037600051600055596000f300",
        nonce=0x00,
        storage={},
    ),
    "0x0000000000000000000000000000000000001004": Account(
        balance=0x0ba1a9ce0ba1a9ce,
        code="0x60ff7ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa600037600051600055596000f300",
        nonce=0x00,
        storage={},
    ),
    "0x0000000000000000000000000000000000001005": Account(
        balance=0x0ba1a9ce0ba1a9ce,
        code="0x60097ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa600037600051600055596000f300",
        nonce=0x00,
        storage={},
    ),
    "0x0000000000000000000000000000000000001010": Account(
        balance=0x0ba1a9ce0ba1a9ce,
        code="0x60016001556001600237",
        nonce=0x00,
        storage={},
    ),
    "0x0000000000000000000000000000000000001011": Account(
        balance=0x0ba1a9ce0ba1a9ce,
        code="0x6005565b005b6042601f536101036000601f3760005180606014600357640badc0ffee60ff55",
        nonce=0x00,
        storage={},
    ),
    "0x000f3df6d732807ef1319fb7b8bb8522d0beac02": Account(
        balance=0x00,
        code="0x3373fffffffffffffffffffffffffffffffffffffffe14604d57602036146024575f5ffd5b5f35801560495762001fff810690815414603c575f5ffd5b62001fff01545f5260205ff35b5f5ffd5b62001fff42064281555f359062001fff015500",
        nonce=0x01,
        storage={0x03e8: 0x03e8},
    ),
    "0xa94f5374fce5edbc8e2a8697c15331677e6ebf0b": Account(
        balance=0x0ba1a9ce0b96f005,
        code="0x",
        nonce=0x01,
        storage={},
    ),
    "0xcccccccccccccccccccccccccccccccccccccccc": Account(
        balance=0x0ba1a9ce0ba1a9cf,
        code="0x701234567890abcdef01234567890abcdef0600052604060206010600f60006004356110000162fffffff15060205160005560405160015500",
        nonce=0x00,
        storage={0x00: 0x3456000000000000000000000000000000000000000000000000000000000000},
    ),
}


def test_calldatacopy(
    state_test: StateTestFiller,
    pre: Alloc,
):

    env = Environment(
        difficulty=0x20000,
        gas_limit=100000000,
        number=1,
        timestamp=1000,
    )

    post = {}

    tx = Transaction(
        data="0x693c61390000000000000000000000000000000000000000000000000000000000000000",
        # gas_limit=0x04c4b400,
        # r=0xe8ff56322287185f6afd3422a825b47bf5c1a4ccf0dc0389cdc03f7c1c32b7ea,
        # s=0x776b02f9f5773238d3ff36b74a123f409cd6420908d7855bbe4c8ff63e00d698,
        to="0xcccccccccccccccccccccccccccccccccccccccc",
        # v=0x1b,
        # value=0x01,
    )

    state_test(env=env, pre=pre, post=local_post, tx=tx)
