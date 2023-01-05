import aiohttp
import asyncio
from aiohttp  import web

routes = web.RouteTableDef()

@routes.get("/proslijedi")
async def proslijedi_pod(request):
    try:
        async with aiohttp.ClientSession() as session:
           
            odg = await session.get("http://127.0.0.1:8080/S0")
            podaci = await odg.json()
            print(len(podaci))
            zad = [
                asyncio.create_task(session.post("http://127.0.0.1:8082/w", json=podaci)),
                asyncio.create_task(session.post("http://127.0.0.1:8083/d", json=podaci))
            ]
            await asyncio.gather(*zad)
            print(zad)

        return web.json_response({"status": "works", "response": podaci}, status=200)
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=500)


app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port=8081)