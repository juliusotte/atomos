import asyncio

from atomos.core.adapters.notification import email


async def main():
    email_notification = email.EMailNotification(
        smtp_host='localhost',
        smtp_port=1025,
    )
    await email_notification.notify('admin@domain.tld', 'hello world')

if __name__ == '__main__':
    asyncio.run(main())
