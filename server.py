from typing import Annotated
from typing import List
#from pythonBackend import run

from starlette.responses import FileResponse
from fastapi import FastAPI, UploadFile, Form, Request
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


class FormSettings(BaseModel):
    title: str
    course: str
    professor: str
    number_of_mcq_questions: int
    number_of_TF_questions: int
    number_of_written_questions: int
    school_type: str
    difficulty: str
    testing_philosophy: str
    subject_material:List[UploadFile]

class QAPair(BaseModel):
    question:str
    answer: str
    type: str

    choices: List[str] = ['T', 'F'] #Holds Choices in a multiple Choice question
    
class GeneratedTest(BaseModel):
    questions:List[QAPair]

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


#Used for converting Multiple Choice Numbers to Letters
def toLetter(num):
    return chr(num + 64)

templates.env.filters['toLetter'] = toLetter

@app.get("/")
def read_index(request: Request):
    return templates.TemplateResponse(
        request=request, name="form.html")

@app.post("/generate")
def final(
    data: Annotated[FormSettings, Form()],request: Request
    
):
    print(data)
    test = run(data)

    fake_response=GeneratedTest(questions=[QAPair(question="What is 2+2?", answer="4", type="written"),QAPair(question="What is 1+2?",answer="3" , type="written"),QAPair(question="What is 1+3?",answer="4" , type="multiple", choices=["1", "2", "3", "4"]), QAPair(question="What is 2+2?", answer="T", type="TF")] )

    return templates.TemplateResponse(
        request=request, name="finshed_test.html", context={"Settings": data,"Test":fake_response}
    )