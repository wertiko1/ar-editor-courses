from __future__ import annotations

import json
import os
import re
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="AR Course Editor API")

COURSES_DIR = Path(os.getenv("COURSES_DIR", "/data/courses"))
COURSES_DIR.mkdir(parents=True, exist_ok=True)

FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent

_SAFE_ID = re.compile(r"^[a-zA-Z0-9_-]{1,128}$")


def _validate_id(course_id: str) -> Path:
    if not _SAFE_ID.match(course_id):
        raise HTTPException(400, "Invalid course id")
    return COURSES_DIR / f"{course_id}.json"


# --------------- Pydantic models ---------------

class Vector2(BaseModel):
    x: float
    y: float


class Vector3(BaseModel):
    x: float
    y: float
    z: float = 1.0


class Color(BaseModel):
    r: float
    g: float
    b: float
    a: float = 1.0


class Step(BaseModel):
    title: str = ""
    description: str = ""
    imageName: str = ""
    audioName: str = ""
    videoName: str = ""
    requireQRVerification: bool = False
    expectedQRText: str = ""
    layoutPreset: int = 0
    customFontName: str = ""
    imagePosition: Vector2 = Vector2(x=600, y=-250)
    imageScale: Vector3 = Vector3(x=1, y=1, z=1)
    imageSize: Vector2 = Vector2(x=500, y=500)
    videoPosition: Vector2 = Vector2(x=0, y=0)
    videoScale: Vector3 = Vector3(x=1, y=1, z=1)
    videoSize: Vector2 = Vector2(x=640, y=360)
    titlePosition: Vector2 = Vector2(x=80, y=-100)
    titleSize: Vector2 = Vector2(x=1000, y=100)
    titleFontSize: float = 45
    titleColor: Color = Color(r=1, g=1, b=1, a=1)
    titleStyle: int = 0
    descPosition: Vector2 = Vector2(x=80, y=-250)
    descSize: Vector2 = Vector2(x=1000, y=400)
    descFontSize: float = 30
    descColor: Color = Color(r=0.85, g=0.85, b=0.85, a=1)
    descStyle: int = 0


class CourseData(BaseModel):
    steps: list[Step]


class CourseInfo(BaseModel):
    id: str
    name: str


# --------------- API ---------------

@app.get("/api/courses", response_model=list[CourseInfo])
async def list_courses():
    return [
        CourseInfo(id=f.stem, name=f.stem)
        for f in sorted(COURSES_DIR.glob("*.json"))
    ]


@app.post("/api/courses")
async def create_course(data: CourseData):
    course_id = uuid4().hex[:8]
    path = COURSES_DIR / f"{course_id}.json"
    path.write_text(json.dumps(data.model_dump(), ensure_ascii=False, indent=2))
    return {"id": course_id}


@app.get("/api/courses/{course_id}")
async def get_course(course_id: str):
    path = _validate_id(course_id)
    if not path.exists():
        raise HTTPException(404, "Course not found")
    return json.loads(path.read_text())


@app.put("/api/courses/{course_id}")
async def update_course(course_id: str, data: CourseData):
    path = _validate_id(course_id)
    if not path.exists():
        raise HTTPException(404, "Course not found")
    path.write_text(json.dumps(data.model_dump(), ensure_ascii=False, indent=2))
    return {"id": course_id}


@app.delete("/api/courses/{course_id}")
async def delete_course(course_id: str):
    path = _validate_id(course_id)
    if not path.exists():
        raise HTTPException(404, "Course not found")
    path.unlink()
    return {"ok": True}


# --------------- Serve frontend ---------------

@app.get("/")
async def index():
    return FileResponse(FRONTEND_DIR / "EditorCourses.html")
