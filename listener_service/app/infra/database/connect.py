from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from infra.config import get_db_url

URL_DATABASE = get_db_url()
engine = create_async_engine(URL_DATABASE)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
