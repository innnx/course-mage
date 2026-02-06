# 第一阶段：编译 (build-stage)
# 使用 Node 镜像进行打包，给它起个别名叫 build-stage
FROM node:20-alpine AS build-stage

WORKDIR /app

# 1. 先拷贝依赖描述文件
COPY package*.json ./

# 2. 安装依赖（使用淘宝镜像加速，国内服务器必备）
RUN npm install --registry=https://registry.npmmirror.com

# 3. 拷贝前端所有源码
COPY . .

# 4. 执行打包命令，生成 dist 目录
RUN npm run build

# 第二阶段：运行 (production-stage)
FROM nginx:alpine

# 从第一阶段 (build-stage) 的目录里，把打好的静态文件拷贝到 Nginx 目录
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 拷贝 Nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]