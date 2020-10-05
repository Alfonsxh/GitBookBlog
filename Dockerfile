FROM fellah/gitbook as builder

WORKDIR /app

RUN npm config set registry https://registry.npm.taobao.org/ 

CMD gitbook build && mv -f ./_book/* /pages/