""" Реализация декоратора для обработки ошибок при работе с gRPC """

from functools import wraps
from fastapi import HTTPException
from app.domain_exceptions import *
from app.core.logging import logger
from app.domain_exceptions.streaming_exceptions import StreamingException


def handle_exceptions(func):
    """ Декоратор для обработки исключений при работе с gRPC """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except InvalidIdException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except UniqueViolationException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except ValueError as e:
            raise HTTPException(status_code=500, detail=str(e))
        except InvalidDescriptionSize as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except InvalidMimeType as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except AgeTooSmallException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except AgeTooBigException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except AgeIncorrectFormat as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except NameTooLongException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except EmptyNameException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except NotRealNameException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except NotExistException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except UniqueException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except NoSuchAlbumException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except NoSuchTrackException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except OwnerAlbumDublicateException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except AlbumTrackDublicateException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except ForbiddenDeletingException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except ForbiddenInsertingException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except UserExistanceException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except SQLConnectException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except InvalidLoginPasswordException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except TokenExistanceException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except IncorrectTokenDataException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except ExpiredTokenException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except DamagedTokenException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except UniqueUserException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except PydanticValidationError as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except StreamingException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except Exception as e:
            # Для неопознанных ошибок
            raise HTTPException(status_code=500, detail=str(e))
    return wrapper
