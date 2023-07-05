# 使用基础镜像，可以根据您的需求选择其他合适的基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 将当前目录下的所有文件复制到工作目录
COPY . /app

# 安装依赖包
RUN pip install --no-cache-dir gunicorn flask kafka-python toml


# 暴露端口
EXPOSE 8000

# 设置启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
