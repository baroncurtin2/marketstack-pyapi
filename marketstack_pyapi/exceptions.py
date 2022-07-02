class RestClientException(Exception):
    """Wrapper exception for RestClientError"""

    pass


class MissingAPIKeyException(Exception):
    """Exception class for missing API key"""

    def __init__(self) -> None:
        super().__init__(
            "MarketStack API Key not provided. Please provide via environment variable or access_key argument"
        )
