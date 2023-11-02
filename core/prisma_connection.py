from prisma import Prisma


async def prisma_connection() -> Prisma:
    prisma_db: Prisma = Prisma()
    return prisma_db
