import uvicorn
from fastapi import FastAPI

from app.api.endpoints import router as api_router
from fastapi.openapi.utils import get_openapi


app = FastAPI()

def custom_openapi():
    # Если схема уже сгенерирована — просто возвращаем её
    if app.openapi_schema:
        return app.openapi_schema

    # Генерируем базовую схему OpenAPI
    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="Документация API с JWT авторизацией",
        routes=app.routes,
    )

    # Добавляем схему авторизации (JWT через заголовок Authorization)
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",  # Authorization: Bearer <token>
            "bearerFormat": "JWT",
        }
    }

    # Применяем авторизацию ко всем ручкам
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]

    # Сохраняем результат
    app.openapi_schema = openapi_schema
    return openapi_schema

app.openapi = custom_openapi
app.include_router(api_router, prefix='/api')



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
