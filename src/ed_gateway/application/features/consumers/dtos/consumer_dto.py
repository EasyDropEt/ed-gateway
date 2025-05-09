from ed_core.documentation.abc_core_api_client import \
    ConsumerDto as CoreConsumerDto


class ConsumerDto(CoreConsumerDto):
    token: str
