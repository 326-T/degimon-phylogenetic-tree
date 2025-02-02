from typing import Annotated
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.service import render, render_selected

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request, img: str = Depends(render)):
    return templates.TemplateResponse(
        "index.html", {"request": request, "img": img}, media_type="text/html"
    )


@app.get("/search")
async def selected(
    request: Request,
    start: str,
    dest: str,
    img: Annotated[str, Depends(render_selected)],
):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "img": img, "start": start, "dest": dest},
        media_type="text/html",
    )
