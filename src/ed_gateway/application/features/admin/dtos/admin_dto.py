from ed_core.documentation.api.abc_core_api_client import \
    AdminDto as CoreAdminDto


class AdminDto(CoreAdminDto):
    token: str
