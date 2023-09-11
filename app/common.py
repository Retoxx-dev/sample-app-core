from enum import Enum


class ErrorCode(str, Enum):
    REGISTER_INVALID_NAME = "REGISTER_INVALID_NAME"
    INVALID_OTP_TOKEN = "INVALID_OTP_TOKEN"
