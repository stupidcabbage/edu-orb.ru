import asyncio
import logging
import sys
from diary.config import db_session
from diary.api.notification import marks_poiling
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
            ])

a = asyncio.run(marks_poiling())
print(a)
