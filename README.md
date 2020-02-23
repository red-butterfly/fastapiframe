## 初始化数据库
修改数据库配置，创建脚本
`alembic revision --autogenerate -m "initdb"`

执行修改
`alembic upgrade head`