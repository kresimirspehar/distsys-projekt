import aiohttp
from aiohttp  import web

routes = web.RouteTableDef()


@routes.post("/d")
async def starts_d(request):
    try:
        async with aiohttp.ClientSession() as session:
            
            data = await request.json()
            #print(len(data))
            filter_d = [row for row in data["data"] if row["username"].startswith("d")]
            #print(len(filter_d))
            x = await session.post("http://127.0.0.1:8084/gatherData", json=filter_d)
            #print(x)

            return web.json_response({"status":"works"}, status=200)
    except Exception as e:
        return web.json_response({"status":"error", "message": str(e)}, status=500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port=8083)