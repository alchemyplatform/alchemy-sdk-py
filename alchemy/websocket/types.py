from alchemy.types import BaseEnum


class EventType(BaseEnum):
    """
    The following event types are accepted in all eth_subscribe WebSocket requests through your Alchemy endpoint.

    :var ALCHEMY_MINED_TRANSACTIONS: Emits full transaction objects or hashes that are mined on the network based on provided filters and block tags.
    :var ALCHEMY_PENDING_TRANSACTIONS: Emits full transaction objects or hashes that are sent to the network, marked as "pending", based on provided filters.
    :var NEW_PENDING_TRANSACTIONS: Emits transaction hashes that are sent to the network and marked as "pending".
    :var NEW_HEADS: Emits new blocks that are added to the blockchain.
    :var LOGS: Emits logs attached to a new block that match certain topic filters.
    """

    ALCHEMY_MINED_TRANSACTIONS = 'alchemy_minedTransactions'
    ALCHEMY_PENDING_TRANSACTIONS = 'alchemy_pendingTransactions'
    NEW_PENDING_TRANSACTIONS = 'newPendingTransactions'
    NEW_HEADS = 'newHeads'
    LOGS = 'logs'
