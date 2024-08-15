from typing import Optional

class StatusCode:
    HTTP_500 = 500

class APIException(Exception):
    status_code: int
    code: str
    message: Optional[str]

    def __init__(
        self,
        *,
        status_code: int = StatusCode.HTTP_500,
        code: str = "000000",
        message: Optional[str] = "오류가 발생했습니다. 시스템 관리자에게 문의해주세요",
    ):
        self.status_code = status_code
        self.code = code
        self.message = message

class IncorrectKeywordError(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=StatusCode.HTTP_401,
            code=f"{StatusCode.HTTP_401}{'3'.zfill(3)}",
            message="지원하지 않는 keyword 입니다.",
        )