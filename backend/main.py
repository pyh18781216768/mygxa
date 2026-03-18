from datetime import datetime, timedelta
from typing import Generator

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import Boolean, DateTime, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

DATABASE_URL = "mysql+pymysql://root:Puyonghao1998@localhost:3306/mygxa"
SLIDER_TOKEN = "slide-pass"
SMS_CODE = "123456"


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    phone: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(128))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

app = FastAPI(title="MyGXA Login API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SendCodeRequest(BaseModel):
    phone: str = Field(min_length=11, max_length=11)
    slider_token: str


class LoginRequest(BaseModel):
    phone: str = Field(min_length=11, max_length=11)
    password: str = Field(min_length=6)
    code: str = Field(min_length=6, max_length=6)
    slider_token: str


class ApiResponse(BaseModel):
    success: bool
    message: str


class LoginResponse(ApiResponse):
    phone: str
    login_at: datetime
    expires_at: datetime


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.phone == "13800138000").first()
        if not existing:
            db.add(User(phone="13800138000", password="Password123"))
            db.commit()
    finally:
        db.close()


@app.get("/api/health", response_model=ApiResponse)
def health() -> ApiResponse:
    return ApiResponse(success=True, message="service ready")


@app.post("/api/send-code", response_model=ApiResponse)
def send_code(payload: SendCodeRequest) -> ApiResponse:
    if payload.slider_token != SLIDER_TOKEN:
        raise HTTPException(status_code=400, detail="滑动验证未通过")
    return ApiResponse(success=True, message=f"验证码已发送，演示验证码：{SMS_CODE}")


@app.post("/api/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    if payload.slider_token != SLIDER_TOKEN:
        raise HTTPException(status_code=400, detail="滑动验证未通过")
    if payload.code != SMS_CODE:
        raise HTTPException(status_code=400, detail="验证码错误")

    user = db.query(User).filter(User.phone == payload.phone, User.is_active.is_(True)).first()
    if not user or user.password != payload.password:
        raise HTTPException(status_code=401, detail="手机号或密码错误")

    login_at = datetime.utcnow()
    expires_at = login_at + timedelta(hours=2)
    return LoginResponse(
        success=True,
        message="登录成功",
        phone=user.phone,
        login_at=login_at,
        expires_at=expires_at,
    )
