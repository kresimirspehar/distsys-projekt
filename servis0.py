import aiohttp
import asyncio
import aiosqlite
import aiofiles
import json
from aiohttp  import web

routes = web.RouteTableDef()

@routes.get("/S0")
async def getS0(request):
    try:
        response = {
            "data": [],
        }

        async with aiosqlite.connect("baza.db") as db:
            async with db.execute("SELECT * FROM podaci LIMIT 100") as cur:
                async for row in cur:
                    data = {'username': row[0], 'ghlink': row[1], 'filename': row[2], 'content': row[3]}
                    #print(data)
                    response["data"].append(data)
            await db.commit()
            print(response)

        return web.json_response(response)
    except Exception as e:
        return web.json_response({"S0": "error", "response": str(e)}, status=500)

async def provjera_baze():
    async with aiosqlite.connect("baza.db") as db:
        print("Provjeravanje baze")

        async with db.execute("SELECT COUNT(*) FROM podaci") as cur:
            count = await cur.fetchone()
            if count[0] == 0:
                print("U bazi nema elemenata")
                await napuni_bazu()

async def napuni_bazu():
    async with aiofiles.open("data.json", mode="r") as file:
        x = 0
        print("Popunjavanje baze...")
        async for row in file:
            data = json.loads(row)
            repo_name = data["repo_name"]
            username, _ = repo_name.split("/")
            ghlink = f"https://github.com/{repo_name}"
            path = data["path"]
            filename = path.split("/")[-1]
            content = data["content"]
            async with aiosqlite.connect("baza.db") as db:
                await db.execute(
                    "INSERT INTO podaci (username,ghlink,filename,content) VALUES (?,?,?,?)",
                    (username, ghlink, filename, content)
                )
                await db.commit()
            x += 1
            if x == 10000:
                return


asyncio.run(provjera_baze())

app = web.Application()

app.router.add_routes(routes)

web.run_app(app)