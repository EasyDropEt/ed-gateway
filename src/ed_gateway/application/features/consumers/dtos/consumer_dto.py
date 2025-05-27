from ed_core.documentation.api.abc_core_api_client import \
    ConsumerDto as CoreConsumerDto


class ConsumerDto(CoreConsumerDto):
    token: str
