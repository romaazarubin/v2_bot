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
        return await self.pool.execute("INSERT INTO client (id, username, status) VALUES ($1, $2, $3)",
                                       str(id),
                                       username, False)

    async def update_status(self, id, status):
        return await self.pool.execute('UPDATE client SET status=$2 where id=$1', str(id), status)

    async def check_status(self, id):
        return await self.pool.fetchval("SELECT status from client where id = $1", str(id))

    async def add_manager(self, username, manager_id, city, department):
        return await self.pool.execute(
            "INSERT INTO manager (username, manager_id, city, department, applications) VALUES ($1,$2,$3,$4,$5)", username, manager_id, city,
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
                                        "From request where department = $4", 'хостинг', 'покупка', 'другое', 'ремонт')

    async def all_client_txt(self):
        return await self.pool.fetch("SELECT username FROM client")

    async def select_manager_day(self, year, month, day):
        return await self.pool.fetch(
            "select username, count(date_req) as applications from manager_app where extract(year from date_req) = $1 and extract(month from date_req) = $2 and extract(day from date_req) = $3 group by username",
            year, month, day)

    async def select_manager_month(self, year, month):
        return await self.pool.fetch(
            "select username, count(date_req) as applications from manager_app where extract(year from date_req) = $1 and extract(month from date_req) = $2 group by username",
            year, month)

    async def select_city_day(self, year, month, day):
        return await self.pool.fetchrow(
            "select count(date_req) as s1, (select count(date_req) as s2 from manager_app where extract(year from date_req) = $1 and extract(month from date_req) = $2 and extract(day from date_req) = $3 and city='Иркутск') from manager_app where extract(year from date_req) = $1 and extract(month from date_req) = $2 and extract(day from date_req) = $3 and city='Москва'",
            year, month, day)

    async def select_city_month(self, year, month):
        return await self.pool.fetchrow("select count(date_req) as s1,"
                                        "(select count(date_req) as s2 from manager_app where extract(year from date_req) = $1 and extract(month from date_req) = $2 and city='Иркутск') "
                                        "from manager_app where extract(year from date_req) = $1 and extract(month from date_req) = $2 and city='Москва'",
                                        year, month)

    async def select_department_day(self, year, month, day):
        return await self.pool.fetchrow("select count(date_req) as s1, "
                                        "(select count(date_req) as s2 from manager_app where extract(year from date_req) = $1 and extract(month from date_req) = $2 and extract(day from date_req) = $3 and department='хостинг'),"
                                        "(select count(date_req) as s3 from manager_app where extract(year from date_req) = $1 and extract(month from date_req) = $2 and extract(day from date_req) = $3 and department='покупка'),"
                                        "(select count(date_req) as s4 from manager_app where extract(year from date_req) = $1 and extract(month from date_req) = $2 and extract(day from date_req) = $3 and department='другое') "
                                        "from manager_app where extract(year from date_req) = $1 and extract(month from date_req) = $2 and extract(day from date_req) = $3 and department='ремонт'",
                                        year, month, day)

    async def select_department_month(self, year, month):
        return await self.pool.fetchrow("select count(date_req) as s1, "
                                        "(select count(date_req) as s2 from manager_app where extract(year from date_req) = $1 and extract(month from date_req) = $2 and department='хостинг'),"
                                        "(select count(date_req) as s3 from manager_app where extract(year from date_req) = $1 and extract(month from date_req) = $2 and department='покупка'),"
                                        "(select count(date_req) as s4 from manager_app where extract(year from date_req) = $1 and extract(month from date_req) = $2 and department='другое') "
                                        "from manager_app where extract(year from date_req) = $1 and extract(month from date_req) = $2 and department='ремонт'",
                                        year, month)

    async def manager_app_add(self, username, date_req, department, city):
        return await self.pool.execute('INSERT INTO manager_app (username, date_req, department, city) VALUES ($1, $2, $3, $4)', username, date_req, department, city)

    async def select_username_client(self, user_id):
        return await self.pool.fetchval("SELECT username from client where id=$1", str(user_id))

    async def select_manager(self, city, department):
        return await self.pool.fetchrow("select username, manager_id from manager where number = (SELECT MIN(number) FROM manager where city like $1 and department like $2)", '%' + str(city) + '%', '%' + str(department) + '%')

    # async def del_manager(self, manager_id):
    #     return await self.pool.execute("DELETE FROM manager WHERE manager_id=$1", str(manager_id))
    #
    # async def comeback_manager(self, username, city, department, applications, manager_id):
    #     return await self.pool.execute(
    #         "INSERT INTO manager (username, manager_id, city, department, applications) VALUES ($1,$2,$3,$4,$5)",
    #         username, manager_id, city,
    #         department, applications)

    async def update_manager(self, manager_id):
        return await self.pool.execute('update manager set number = (select max(number) from manager) + 1, applications = applications+1 where manager_id = $1', manager_id)

