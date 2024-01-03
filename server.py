from sanic import Sanic
from sanic.response import text

app = Sanic("myapp")

@app.route('/')
async def hello(request):
    return text('Merhaba, Sanic!')


async def mainfunc(request):
    print(request.json)
    return text("OK")

app.add_route(mainfunc,"/send", methods=["POST"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
