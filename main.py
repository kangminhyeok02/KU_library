from fastapi import FastAPI, HTTPException, Query
from fastapi.templating import Jinja2Templates
from fastapi import Request
import psycopg2
from datetime import datetime, timedelta
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, JSONResponse


from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html",{"request":request})

@app.get("/main/")
async def home(request: Request):
    return templates.TemplateResponse("main.html",{"request":request})

@app.get("/search/")
async def home(request: Request):
    return templates.TemplateResponse("search.html",{"request":request})


@app.get("/search_get/")
async def home(request: Request):
    return templates.TemplateResponse("search_get.html",{"request":request})

@app.get("/insert/")
async def home(request: Request):
    return templates.TemplateResponse("insert.html",{"request":request})

@app.get("/search_info/")
async def home(request: Request):
    return templates.TemplateResponse("search_info.html",{"request":request})


@app.get("/search_book/")
async def home(request: Request):
    return templates.TemplateResponse("search_book.html",{"request":request})



@app.get("/search_money/")
async def home(request: Request):
    return templates.TemplateResponse("search_money.html",{"request":request})


@app.get("/search_period/")
async def home(request: Request):
    return templates.TemplateResponse("search_period.html",{"request":request})



@app.get("/search_phone/")
async def home(request: Request):
    return templates.TemplateResponse("search_phone.html",{"request":request})



@app.get("/login/")
async def home(request: Request):
    return templates.TemplateResponse("login.html",{"request":request})


@app.get("/search_phone_C/")
async def home(request: Request):
    return templates.TemplateResponse("search_phone_C.html",{"request":request})

@app.get("/search_phone_B/")
async def home(request: Request):
    return templates.TemplateResponse("search_phone_B.html",{"request":request})


@app.get("/search_phone_A/")
async def home(request: Request):
    return templates.TemplateResponse("search_phone_A.html",{"request":request})


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

import pymysql

conn = pymysql.connect(host="127.0.0.1", user="root", password="020330", 
                        db='test12312312312', charset="utf8", cursorclass=pymysql.cursors.DictCursor)
cur = conn.cursor()





@app.get("/userInfo/")
def getUserInfoByName():
  sql = "SELECT * FROM 회원"
  cur.execute(sql)
  row = cur.fetchall()
  print(row)
  return row


@app.get("/user대여/")
def getUserInfoByNumberAndName(memberId: str = Query(..., description="회원번호를 입력하세요"), memberName: str = Query(..., description="회원이름을 입력하세요")):
    try:
        print(f"Received 회원번호: {memberId}, 회원명: {memberName}")
        
        # 회원 정보 조회
        cur.execute("SELECT * FROM 회원 WHERE 회원번호 = %s AND 회원명 = %s", (memberId, memberName))
        member_info = cur.fetchall()

        if not member_info:
            raise HTTPException(status_code=404, detail="User not found")

        # 대출 정보 조회
        cur.execute("SELECT 도서번호, 대출일자 FROM 대여 WHERE 회원번호 = %s", (memberId,))
        loan_info = cur.fetchall()

        if not loan_info:
            raise HTTPException(status_code=404, detail="No loan data found for this user")

        # 결과 조합
        result = {
            "loan_info": loan_info
        }
        
        return result
    
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    


@app.get("/user예약/")
def getUserInfoByNumberAndName(memberId: str = Query(..., description="회원번호를 입력하세요"), memberName: str = Query(..., description="회원이름을 입력하세요")):
    try:
        print(f"Received 회원번호: {memberId}, 회원이름: {memberName}")
        
        # 회원 정보 조회
        cur.execute("SELECT 회원등급 FROM 회원 WHERE 회원번호 = %s AND 회원명 = %s", (memberId, memberName))
        member_info = cur.fetchone()

        if not member_info:
            raise HTTPException(status_code=404, detail="User not found")
        
        # 대출 정보 조회
        cur.execute("SELECT 도서번호, 예약일시 FROM 예약 WHERE 회원번호 = %s", (memberId,))
        loan_info = cur.fetchall()

        if not loan_info:
            raise HTTPException(status_code=404, detail="No loan data found for this user")

        # 결과 조합
        result = {
            "loan_info": loan_info
        }
        
        return result
    
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    


@app.get("/bookInfo/")
def getBookInfo(bookId: str = Query(..., description="도서번호를 입력하세요")):
    try:
        print(f"Received 도서번호: {bookId}")
        
        # 도서 재고량 확인
        cur.execute("SELECT 재고량 FROM 도서 WHERE 도서번호 = %s", (bookId,))
        stock = cur.fetchone()
        
        if not stock:
            return {
                "message": "이 책은 도서관에 없습니다"
            }
        
        if stock['재고량'] == 0:
            result = {
                "message": "현재 도서의 재고량이 0입니다.  도서를 대출할 수 없습니다. 예약하세요"
            }
        else:
            # 도서 정보 조회
            cur.execute("SELECT ISBN, 저자, 출판사 FROM 도서정보 WHERE ISBN = (SELECT ISBN FROM 도서 WHERE 도서번호 = %s)", (bookId,))
            book_info = cur.fetchone()
            result = {
                "ISBN": book_info['ISBN'],
                "저자": book_info['저자'],
                "출판사": book_info['출판사']
        
            }
        
        return result
    
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

from datetime import datetime
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import sqlite3


class LoanInfo(BaseModel):
    memberId: str
    rentalDate: str
    returnDate: str
    numBooks: int

def 대여_시간_계산(대출일자, 반납일자):
    대출일자_객체 = datetime.strptime(대출일자, "%Y-%m-%d")
    반납일자_객체 = datetime.strptime(반납일자, "%Y-%m-%d")
    대여_시간 = (반납일자_객체 - 대출일자_객체).days
    return 대여_시간

def 규칙_확인(회원_등급, 대여_시간):
    규칙 = {
        'A': [
            {'대여_시간': lambda x: x <= 7, '무료_대여': True, '연체료_5000원': False, '연체료_10000원': False, '블랙리스트': False},
            {'대여_시간': lambda x: x > 7, '무료_대여': False, '연체료_5000원': True, '연체료_10000원': False, '블랙리스트': False}
        ],
        'B': [
            {'대여_시간': lambda x: x <= 7, '무료_대여': True, '연체료_5000원': False, '연체료_10000원': False, '블랙리스트': False},
            {'대여_시간': lambda x: 7 < x <= 14, '무료_대여': False, '연체료_5000원': True, '연체료_10000원': False, '블랙리스트': False},
            {'대여_시간': lambda x: x > 14, '무료_대여': False, '연체료_5000원': False, '연체료_10000원': True, '블랙리스트': False}
        ],
        'C': [
            {'대여_시간': lambda x: x <= 7, '무료_대여': True, '연체료_5000원': False, '연체료_10000원': False, '블랙리스트': False},
            {'대여_시간': lambda x: 7 < x <= 14, '무료_대여': False, '연체료_5000원': False, '연체료_10000원': True, '블랙리스트': False},
            {'대여_시간': lambda x: x > 14, '무료_대여': False, '연체료_5000원': False, '연체료_10000원': False, '블랙리스트': True}
        ]
    }

    for rule in 규칙[회원_등급]:
        if rule['대여_시간'](대여_시간):
            return {
                '무료_대여': rule['무료_대여'],
                '연체료_5000원': rule['연체료_5000원'],
                '연체료_10000원': rule['연체료_10000원'],
                '블랙리스트': rule['블랙리스트']
            }
    return None  # 해당 규칙이 없을 경우

@app.post("/calculateLateFee/")
def calculateLateFee(info: LoanInfo):
    try:
        대여_시간 = 대여_시간_계산(info.rentalDate, info.returnDate)
        
        # 회원 등급 조회
        cur.execute("SELECT 회원등급 FROM 회원 WHERE 회원번호 = %s", (info.memberId,))
        member_grade = cur.fetchone()
        
        if not member_grade:
            raise HTTPException(status_code=404, detail="Member not found")
        
        # 규칙 확인
        rule = 규칙_확인(member_grade['회원등급'], 대여_시간)
        
        if rule['블랙리스트']:
            return {"late_fee": "회원이 블랙리스트에 등재되었습니다."}
        
        연체료 = 0
        if rule['연체료_5000원']:
            연체료 = 5000 * info.numBooks
        elif rule['연체료_10000원']:
            연체료 = 10000 * info.numBooks
        
        return {"late_fee": 연체료}
    
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))




class BookInfoRequest(BaseModel):
    member_name: str
    book_title: str
    
class PhoneNumberRequest(BaseModel):
    phone_number: str
    
    
# 각 회원 등급별 엔드포인트 추가
@app.get("/search_phone_A/")
def search_phone_A(phone_number: str):
    return {"message": f"회원 등급 A의 전화번호 {phone_number}가 제출되었습니다."}

@app.get("/search_phone_B/")
def search_phone_B(phone_number: str):
    return {"message": f"회원 등급 B의 전화번호 {phone_number}가 제출되었습니다."}

@app.get("/search_phone_C/")
def search_phone_C(phone_number: str):
    return {"message": f"회원 등급 C의 전화번호 {phone_number}가 제출되었습니다."}

@app.get("/check_book_status/")

def check_book_status(member_name: str, book_title: str):
    try:
        print(f"Received member_name: {member_name}, book_title: {book_title}")

        # 회원번호 및 회원 등급 추정
        cur.execute("SELECT 회원번호, 회원등급 FROM 회원 WHERE 회원명 = %s", (member_name,))
        member_result = cur.fetchone()
        print(f"member_result: {member_result}")
        
        if not member_result:
            return {"message": "해당 회원을 찾을 수 없습니다."}
        
        member_id = member_result['회원번호']
        member_grade = member_result['회원등급']
        
        # 도서번호 추정
        cur.execute("SELECT 도서번호 FROM 도서 WHERE ISBN = (SELECT ISBN FROM 도서정보 WHERE 도서명 = %s)", (book_title,))
        book_result = cur.fetchone()
        print(f"book_result: {book_result}")
        
        if not book_result:
            return {"message": "해당 도서를 찾을 수 없습니다."}
        
        book_id = book_result['도서번호']
        
        # 대여 릴레이션 확인
        cur.execute("SELECT * FROM 대여 WHERE 회원번호 = %s AND 도서번호 = %s", (member_id, book_id))
        rental_result = cur.fetchone()
        print(f"rental_result: {rental_result}")
        
        if rental_result:
            return {"message": "이미 대여중인 도서입니다.", "member_grade": member_grade}
        
        # 예약 릴레이션 확인
        cur.execute("SELECT * FROM 예약 WHERE 회원번호 = %s AND 도서번호 = %s", (member_id, book_id))
        reservation_result = cur.fetchone()
        print(f"reservation_result: {reservation_result}")
        
        if reservation_result:
            return {"message": "이미 예약중인 도서입니다.", "member_grade": member_grade}
        
        return {"message": "대여 또는 예약되지 않은 도서입니다.", "member_grade": member_grade}
    
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    




def get_member_grade(phone_number):

    cur.execute("SELECT 회원등급 FROM 회원 WHERE 전화번호 = %s", (phone_number,))
    result = cur.fetchone()
    
    if result:
        return result
    else:
        return None



@app.get("/get_member_grade")
async def get_member_grade_route(phone_number: str = Query(..., description="회원의 전화번호")):
    member_grade = get_member_grade(phone_number)
    if member_grade:
        return {"member_grade": member_grade}
    else:
        raise HTTPException(status_code=404, detail="회원 정보를 찾을 수 없습니다.")
  



