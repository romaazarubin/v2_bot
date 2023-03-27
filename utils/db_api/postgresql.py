import asyncio
import asyncpg
from config import ip, PGUSER, PGPASSWORD, DATABASE


class DataBase:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.pool = loop.run_until_complete(
            asyncpg.create_pool(
                database=DATABASE,
                user=PGUSER,
                password=PGPASSWORD,
                host=ip,
                port='5432',
                ssl=False

            )
        )

    async def check_city(self, username):
        return await self.pool.fetchrow("SELECT city, department FROM manager WHERE username = $1", str(username))

    async def presence_user(self, id):
        return await self.pool.fetchval("SELECT EXISTS(SELECT id FROM client WHERE id = $1)", str(id))

    async def add_user(self, id, username):
        return await self.pool.execute("INSERT INTO client (id, username, status) VALUES ($1, $2, $3)", str(id),
                                       username, False)

    async def update_status(self, id, status):
        return await self.pool.execute('UPDATE client SET status=$2 where id=$1', str(id), status)

    async def check_status(self, id):
        return await self.pool.fetchval("SELECT status from client where id = $1", str(id))

    async def add_manager(self, username, city, department):
        return await self.pool.execute(
            "INSERT INTO manager (username, city, department, applications) VALUES ($1,$2,$3,$4)", username, city,
            department, 0)

    async def presence_manager(self, username):
        return await self.pool.fetchval("SELECT EXISTS(SELECT username FROM manager WHERE username = $1)",
                                        str(username))

    async def count_manager(self):
        return await self.pool.fetchval("SELECT count(*) FROM manager")

    async def delete_manager(self, username, city):
        return await self.pool.execute("DELETE FROM manager WHERE username=$1 and city=$2", str(username), city)

    async def all_manager(self, k):
        return await self.pool.fetch("SELECT username, city FROM manager LIMIT $1 OFFSET $2", 5, k)

    async def update_applications(self, username):
        return await self.pool.execute('UPDATE manager SET applications=applications+1 where username=$1',
                                       str(username))

    async def select_applications(self):
        return await self.pool.fetch('SELECT username, applications FROM manager')

    async def all_client(self, k):
        return await self.pool.fetch("SELECT username FROM client LIMIT $1 OFFSET $2", 5, k)

    async def count_client(self):
        return await self.pool.fetchval("SELECT count(*) FROM client")

    async def add_request(self, id, city, department):
        return await self.pool.execute("INSERT INTO request (id, city, department) VALUES ($1, $2, $3)", str(id), city,
                                       department)

    async def count_city_irkutsk(self):
        return await self.pool.fetchval("SELECT count(*) FROM request where city=$1", "Иркутск")

    async def count_city_moscow(self):
        return await self.pool.fetchval("SELECT count(*) FROM request where city=$1", "Москва")

    async def count_city(self):
        return await self.pool.fetchrow(
            "SELECT count(*) as s1, (SELECT count(*) as s2 FROM request WHERE city = $1) From request where city = $2",
            "Иркутск", "Москва")

    async def count_department(self):
        return await self.pool.fetchrow("SELECT count(*) as s1,"
                                        "(SELECT count(*) as s2 FROM request WHERE department = $1),"
                                        "(SELECT count(*) as s3 FROM request WHERE department = $2),"
                                        "(SELECT count(*) as s4 FROM request WHERE department = $3)"
                                        "From request where department = $4",'хостинг', 'покупка', 'ремонт', 'другое')


    async def all_client_txt(self):
        return await self.pool.fetch("SELECT username FROM client")
