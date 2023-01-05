import aiohttp
from aiohttp  import web

routes = web.RouteTableDef()


@routes.post("/w")
async def starts_w(request):
    try:
        async with aiohttp.ClientSession() as session:
            
            data = await request.json()
            #print(len(data))
            filter_w = [row for row in data["data"] if row["username"].startswith("w")]
            #print(len(filter_w))
            x = await session.post("http://127.0.0.1:8084/gatherData", json=filter_w)
            #print(x)

            return web.json_response({"status":"works"}, status=200)
    except Exception as e:
        return web.json_response({"status":"error", "message": str(e)}, status=500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port=8082)