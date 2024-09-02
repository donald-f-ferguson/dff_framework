from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class CourseSection(BaseModel):
    course_id: Optional[int] = None
    course_name: Optional[str] = None
    uuid: Optional[str] = None
    created_at: Optional[str] = None
    course_code: Optional[str] = None
    sis_course_id: Optional[str] = None
    course_no: Optional[str] = None
    section: Optional[str] = None
    course_year: Optional[str] = None
    semester: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "course_id": 123,
                "course_name": "Introduction to Python",
                "uuid": "a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6",
                "created_at": "2023-09-02T12:34:56Z",
                "course_code": "PY101",
                "sis_course_id": "SIS001",
                "course_no": "101",
                "section": "A",
                "course_year": "2024",
                "semester": "Fall"
            }
        }
