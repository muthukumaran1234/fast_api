from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "mobile_no" VARCHAR(20)  UNIQUE;
        ALTER TABLE "user" ADD "password" VARCHAR(100);
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_user_mobile__0cc396" ON "user" ("mobile_no");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_user_mobile__0cc396";
        ALTER TABLE "user" DROP COLUMN "mobile_no";
        ALTER TABLE "user" DROP COLUMN "password";"""
