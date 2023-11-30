import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import getenv as get_env

from dotenv import load_dotenv


class Gmail:
    load_dotenv()

    user: str = get_env("EMAIL")
    password: str = get_env("PASSWORD")

    @staticmethod
    def body(incident: str) -> str:
        with io.open(file=r"src\domain\body.html", encoding="utf-8") as file:
            body: str = file.read()
            body.format(incident)

            return body

    @classmethod
    def send(
        cls,
        incident: str,
        receiver: str,
        subject: str,
    ) -> None:
        message: MIMEMultipart = MIMEMultipart()

        message["From"] = cls.user
        message["To"] = receiver
        message["Subject"] = subject

        message.attach(
            payload=MIMEText(
                _text=cls.body(incident=incident),
                _subtype="html",
            ),
        )

        server = smtplib.SMTP("smtp.gmail.com: 587")
        server.starttls()

        server.login(
            user=cls.user,
            password=cls.password,
        )

        server.sendmail(
            from_addr=message["From"],
            to_addrs=[message["To"]],
            msg=message.as_string().encode("utf-8"),
        )
        server.quit()
