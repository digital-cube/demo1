#!/usr/bin/env python
import base

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from base import orm


@base.route()
class AboutHandler(base.Base):

    @base.api()
    async def get(self):
        return {'name': 'users'}


if __name__ == "__main__":
    import config

    base.run(port=config.port)
