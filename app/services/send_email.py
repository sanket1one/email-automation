import aiosmtplib
import asyncio
import dns.resolver
import ssl
from email.mime.text import MIMEText
from email.message import EmailMessage
from core.config import mail_settings, logger
import copy

SMPT_HOST="localhost"
SMTP_PORT=  8025     #587
IMPLICIT_TLS_PORT = 465
SMTP_TIMEOUT = 30

SENDER = mail_settings.FROM_EMAIL
RECEPIENT = "sanket.patil20@vit.edu"

# mx-(Mail Exchanger) records are used to route emails to the correct server
async def get_primary_mx(domain: str) -> any:
    answers = dns.resolver.resolve(domain, 'MX')
    mx_hosts = sorted([ (rdata.preference, str(rdata.exchange).rstrip('.')) for rdata in answers])
    logger.debug(f"MX records for {domain}: {mx_hosts}")
    return mx_hosts[0][1]


async def optimized_bulk_email(
    sender: str,
    recipient_list: list[str],
    subject: str ,
    body: str,
    use_implicit_tls: bool = False,   
):
    # .1 Lookup MX once per domain
    # domain = recipient_list[0].split("@")[-1]
    # mx_host = await get_primary_mx(domain)
    # logger.info(f"MX host for {domain}: {mx_host}")   

    mx_host = "localhost"

    # 2. Configure SMTP client
    if use_implicit_tls:
        smtp = aiosmtplib.SMTP(
            hostname=mx_host,
            port=IMPLICIT_TLS_PORT,
            use_tls = True,
            tls_context = ssl.create_default_context(),
            timeout=SMTP_TIMEOUT
        )
        await smtp.connect()
        await smtp.ehlo()
        logger.info("Connected with implicit TLS to %s:%d", mx_host, IMPLICIT_TLS_PORT)
    else:
        smtp = aiosmtplib.SMTP(
            hostname = mx_host,
            port = SMTP_PORT,
            timeout = SMTP_TIMEOUT
        )
        await smtp.connect()
        await smtp.ehlo()
        logger.info("Connected with explicit TLS to %s:%d", mx_host, SMTP_PORT)

        # # 3. Enforcce STARTTLS support
        # if not smtp.supports_extension("STARTTLS"):
        #     await smtp.quit()
        #     logger.error("TLS required but unsupported by %s", mx_host)
        #     raise RuntimeError(f"TLS required but unsupported by {mx_host}")

        # # 4. Upgrade connection to TLS
        # await smtp.starttls()
        # await smtp.ehlo()
        # logger.info("Upgraded connection to TLS with STARTTLS")
    
    # 5. Prepare the base message
    base_msg = EmailMessage()
    base_msg["From"] = sender
    base_msg["Subject"] = subject 
    base_msg.set_content(body)

    # 6. Send emails to all recipients: with retry logic
    async def send_to(recipient: str):
        msg = copy.deepcopy(base_msg)
        msg["To"] = recipient
        for attempt in range(3):
            try:
                await asyncio.wait_for(smtp.send_message(msg), timeout=10)
                logger.info("Email sent to %s", recipient)
                break
            except (asyncio.TimeoutError, aiosmtplib.SMTPException) as e:
                if attempt < 2:
                    backoff = 2 ** attempt
                    logger.warning(
                        "Attempt %d to %s failed (%s), retrying in %ds",
                        attempt + 1, recipient, e, backoff
                    )
                    await asyncio.sleep(backoff)
                else:
                    logger.error("Failed to send email to %s after 3 attempts", recipient)
                    raise
    await asyncio.gather(*(send_to(rcpt) for rcpt in recipient_list))

    # 7. Clean up
    await smtp.quit()
    logger.info("SMTP connection closed")


    

if __name__ == "__main__":
   asyncio.run(
        optimized_bulk_email(
            sender=mail_settings.FROM_EMAIL,
            recipient_list=["sanket.patil20@vit.edu"],
            subject="Inquiry About Position Opportunity",
            body="Hello,\n\nI’d like to discuss open roles...\n",
            use_implicit_tls=False   # set True to use port 465 implicit TLS
        )
    )