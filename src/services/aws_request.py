import urllib
from urllib.error import HTTPError
from urllib.request import urlopen

import feedparser
from boto3 import Session

from src.interfaces.service import Service


class AWSRequest(Service):
    response: dict = {}

    session: Session = Session()
    aws_base_status_RSS: str = "https://status.aws.amazon.com/rss/"
    services_list: list[str] = session.get_available_services()

    @classmethod
    def setup_response(
        cls,
        service: str,
        status: bool,
        last_updated: str,
    ) -> None:
        cls.response[service] = {
            "status": status,
            "last_update": last_updated,
        }

    @classmethod
    def parse_rss_feed(
        cls,
        rss_feed: str,
    ) -> None:
        awsfeed = feedparser.parse(rss_feed)

        feed = awsfeed["feed"]
        items = awsfeed["items"]
        service = feed["title"]
        last_updated = awsfeed["updated"]

        if not items:
            status = True
        else:
            status = False

        cls.setup_response(
            service=service,
            status=status,
            last_updated=last_updated,
        )

    @classmethod
    async def get_service_status_by_region(
        cls,
        service: str,
        region: str,
    ) -> None:
        rss_feed_url: str = cls.aws_base_status_RSS + service + "-" + region + ".rss"

        try:
            urlopen(rss_feed_url).getcode()

        except urllib.error.HTTPError as e:
            if hasattr(e, "reason"):
                return
            elif hasattr(e, "code"):
                return

        else:
            cls.parse_rss_feed(rss_feed_url)

    @classmethod
    async def services(cls) -> [dict]:
        sao_paulo: str = "sa-east-1"
        nvirginia: str = "us-east-1"

        for service in cls.services_list:
            await cls.get_service_status_by_region(
                service=service,
                region=nvirginia,
            )

            await cls.get_service_status_by_region(
                service=service,
                region=sao_paulo,
            )

            print(cls.response)

        return cls.response
