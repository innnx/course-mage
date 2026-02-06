# 使用 Nginx 镜像作为基础
FROM nginx:alpine

# 将打包好的 dist 文件夹内容拷贝到 Nginx 运行目录
COPY dist/ /usr/share/nginx/html/

# 将你的 nginx.conf 拷贝进去代替默认配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80