from aiohttp  import web
import aiofiles
import os


routes = web.RouteTableDef()

podaci = []

async def popuni_dat():
    if not os.path.exists('datoteke'):
        os.makedirs('datoteke')
        
    print("write")
    for data in podaci:
        filename = data['filename']
        content = data['content']
        async with aiofiles.open(f'datoteke/{filename}', 'w', encoding='utf-8') as mine:
            await mine.write(content)

@routes.post("/gatherData")
async def gatherData(request):
    try:
        print("gathering")
        data = await request.json()
        podaci.extend(data)
        if len(podaci) > 10:
            await popuni_dat()

        return web.json_response({"status": "works"}, status=200)
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=500)

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8084)