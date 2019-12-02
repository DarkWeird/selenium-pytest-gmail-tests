FROM python:3.6

RUN pip install pytest selenium allure-pytest && mkdir -p /autotests
COPY . /autotests
WORKDIR /autotests

ENTRYPOINT ./wait-for-it.sh $(echo $WD_URL |  sed -E 's#https?://([^/]+?)(/|$).*$#\1#') -- py.test --alluredir=/tmp/allure tests/tests.py && ls /tmp/allure ## you can export allures from here.