FROM python:3.8-slim-buster
WORKDIR /user/src/app
COPY . .
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple  --no-cache-dir
CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]