"""
Handled custom exceptions raised by transaction.
"""


class TransactionError(Exception):
    """
    *400* `Transaction error`

    Raise if a transaction is performed without success
    """

    def __init__(self, error):
        """
        Transaction error
        """
        super().__init__()
        self.error = error
        self.status_code = 400
