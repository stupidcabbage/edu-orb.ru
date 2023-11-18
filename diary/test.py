import asyncio
import logging
import sys
from diary.config import db_session
from diary.api.class_notification import MarkNotification
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
            ])

notification = MarkNotification(db_session)
a = asyncio.run(notification.start_poiling())
print(a)
