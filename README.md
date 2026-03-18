# MyGXA 登录页面示例

这是一个最小可运行的登录页面示例，包含：

- Python FastAPI 后端
- Vue 3 + Vite 前端
- MySQL 数据库配置
- 手机号 + 密码 + 短信验证码 + 滑动验证 登录流程

## 后端启动

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

默认数据库连接：`mysql+pymysql://root:Puyonghao1998@localhost:3306/mygxa`

## 前端启动

```bash
cd frontend
npm install
npm run dev
```

## 演示账号

- 手机号：`13800138000`
- 密码：`Password123`
- 验证码：`123456`
- 滑动验证：拖动到最右侧

## 建表

可执行 `backend/schema.sql` 初始化数据库。
