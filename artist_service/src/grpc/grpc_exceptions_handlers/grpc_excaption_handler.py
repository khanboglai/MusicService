from functools import wraps
import grpc
from src.domain_exceptions import *
from src.core.logging import logger


def grpc_exception_handler(func):
    @wraps(func)
    async def wrapper(self, request, context):
        try:
            return await func(self, request, context)
        except UniqueViolationException as e:
            logger.error(e)
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details(str(e))
            return None
        except InvalidIdException as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(str(e))
            return None
        except InvalidDescriptionSize as e:
            logger.error(e)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return None
        except DatabaseException as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None
        except Exception as e:
            logger.error(e)
            # Обработка всех остальных исключений (если необходимо)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal Server Error")
            return None

        response_type = func.__annotations__.get("return")
        if response_type:
            return response_type()
        return None

    return wrapper
