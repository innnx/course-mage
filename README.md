# CourseHub - 课程管理系统

基于 Spring Boot 3 + Vue 3 的全栈课程管理系统，支持课程管理、订单管理、用户认证等功能。

## 技术栈

### 后端
- **框架**: Spring Boot 3.2.0
- **语言**: Java 17
- **数据库**: MySQL 8.0
- **缓存**: Redis
- **ORM**: MyBatis-Plus 3.5.5
- **安全**: Spring Security + JWT
- **API文档**: SpringDoc OpenAPI (Swagger)

### 前端
- **框架**: Vue 3.5.24 (Composition API)
- **构建工具**: Vite 7.2.4
- **路由**: Vue Router 4.6.4
- **状态管理**: Pinia 3.0.4
- **HTTP客户端**: Axios 1.13.2
- **UI样式**: Tailwind CSS 3.4.19
- **图标**: @heroicons/vue 2.2.0

## 功能特性

### 用户认证
- ✅ 用户注册（支持学生、教师角色）
- ✅ 用户登录（JWT Token 认证）
- ✅ 密码强度验证（8-20位，包含大小写字母和数字）
- ✅ 用户名格式验证（4-20位字母、数字、下划线）

### 课程模块
- ✅ 课程列表展示（分页、搜索、筛选）
- ✅ 课程详情查看
- ✅ 课程创建（教师）
- ✅ 课程编辑（教师）
- ✅ 课程删除（教师）
- ✅ 课程上架/下架（教师）
- ✅ 分类管理（管理员）
- ✅ 学生数统计

### 订单模块
- ✅ 订单创建（购买课程）
- ✅ 订单支付
- ✅ 订单取消
- ✅ 我的订单（学生）
- ✅ 订单管理（管理员）
- ✅ 订单状态筛选
- ✅ 购买状态检查（防重复购买）

### 管理后台
- ✅ 课程管理（CRUD + 上架下架）
- ✅ 分类管理（CRUD + 排序）
- ✅ 订单管理（查看所有订单 + 状态管理）
- ✅ 数据统计卡片
- ✅ 角色权限控制

## 快速开始

### 环境要求
- JDK 17+
- Node.js 18+
- MySQL 8.0+
- Redis 6.0+
- Maven 3.8+

### 后端启动

1. **克隆项目**
```bash
git clone <repository-url>
cd course-mage
```

2. **配置数据库**
```sql
CREATE DATABASE course_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. **修改配置文件**
编辑 `src/main/resources/application.yml`:
```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/course_db?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
    username: root
    password: your_password
  data:
    redis:
      host: localhost
      port: 6379
      password: your_redis_password
```

4. **启动后端**
```bash
mvn clean package
mvn spring-boot:run
```

后端服务将在 `http://localhost:8080` 启动

### 前端启动

1. **安装依赖**
```bash
cd frontend-vue
npm install
```

2. **开发模式**
```bash
npm run dev
```

前端服务将在 `http://localhost:5173` 启动

3. **生产构建**
```bash
npm run build
```

构建产物在 `frontend-vue/dist` 目录

### Docker 部署

使用 docker-compose 一键启动所有服务：
```bash
docker-compose up -d
```

## API 文档

启动后端后访问：
- **Swagger UI**: http://localhost:8080/swagger-ui.html
- **OpenAPI JSON**: http://localhost:8080/v3/api-docs

### 主要接口

#### 认证接口
- `POST /api/user/login` - 用户登录
- `POST /api/user/register` - 用户注册

#### 课程接口
- `GET /api/course/page` - 分页查询课程
- `GET /api/course/{id}` - 获取课程详情
- `POST /api/course` - 创建课程（教师）
- `PUT /api/course` - 更新课程（教师）
- `DELETE /api/course/{id}` - 删除课程（教师）
- `PUT /api/course/{id}/status` - 上架/下架课程（教师）

#### 订单接口
- `POST /api/order` - 创建订单
- `PUT /api/order/{orderNo}/pay` - 支付订单
- `PUT /api/order/{orderNo}/cancel` - 取消订单
- `GET /api/order/my` - 查询我的订单
- `GET /api/order/all` - 查询所有订单（管理员）
- `GET /api/order/{orderNo}` - 获取订单详情
- `GET /api/order/check/{courseId}` - 检查是否购买过课程

#### 分类接口
- `GET /api/category/list` - 获取所有分类
- `POST /api/category` - 创建分类（管理员）
- `PUT /api/category` - 更新分类（管理员）
- `DELETE /api/category/{id}` - 删除分类（管理员）

## 项目结构

```
course-mage/
├── src/main/java/com/course/
│   ├── common/           # 公共模块
│   │   ├── constant/    # 常量定义
│   │   ├── exception/   # 异常处理
│   │   └── result/      # 统一响应结果
│   ├── config/          # 配置类
│   ├── controller/      # 控制器层
│   ├── dto/            # 数据传输对象
│   ├── entity/         # 实体类
│   ├── mapper/         # 数据访问层
│   ├── service/        # 服务层
│   └── utils/          # 工具类
├── src/main/resources/
│   └── application.yml # 配置文件
├── frontend-vue/       # 前端项目
│   ├── src/
│   │   ├── api/       # API 服务
│   │   ├── components/ # 公共组件
│   │   ├── router/    # 路由配置
│   │   ├── stores/    # Pinia 状态管理
│   │   ├── views/     # 页面组件
│   │   └── main.js    # 入口文件
│   ├── package.json
│   └── vite.config.js
└── pom.xml            # Maven 配置
```

## 数据库设计

### 用户表 (user)
- id: 用户ID
- username: 用户名
- password: 密码
- nickname: 昵称
- role: 角色（STUDENT/TEACHER/ADMIN）
- phone: 手机号
- email: 邮箱

### 课程表 (course)
- id: 课程ID
- title: 课程标题
- description: 课程描述
- cover_image: 封面图片
- price: 价格
- category_id: 分类ID
- teacher_id: 教师ID
- student_count: 学生数
- status: 状态（1上架/0下架）
- create_time: 创建时间

### 分类表 (category)
- id: 分类ID
- name: 分类名称
- sort: 排序
- create_time: 创建时间

### 订单表 (course_order)
- id: 订单ID
- order_no: 订单号
- user_id: 用户ID
- course_id: 课程ID
- price: 价格
- status: 状态（0待支付/1已支付/2已取消）
- pay_time: 支付时间
- create_time: 创建时间

## 开发指南

### 后端开发规范

#### Controller 层
```java
@Tag(name = "描述")
@RestController
@RequestMapping("/api/resource")
@RequiredArgsConstructor
public class ResourceController {
    private final ResourceService resourceService;

    @Operation(summary = "描述")
    @PostMapping
    public Result<Void> create(@Valid @RequestBody RequestDto request) {
        resourceService.create(request);
        return Result.success();
    }
}
```

#### Service 层
- 使用 `@Service` 注解
- 使用接口 + 实现模式
- 抛出 `BusinessException` 处理业务错误
- 使用 `LambdaQueryWrapper` 进行 MyBatis-Plus 查询

#### 异常处理
```java
throw new BusinessException("错误消息");
throw new BusinessException(400, "自定义错误码");
```

#### 测试
```bash
# 运行所有测试
mvn test

# 运行单个测试类
mvn test -Dtest=ClassName

# 运行单个测试方法
mvn test -Dtest=ClassName#methodName
```

### 前端开发规范

#### 组件开发
```vue
<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();
const loading = ref(true);
const data = ref([]);

onMounted(() => {
  fetchData();
});
</script>
```

#### API 调用
```javascript
import { courseAPI } from '../api/services';

const data = await courseAPI.getList({ pageNum: 1, pageSize: 10 });
```

#### 路由守卫
- 使用 `meta: { requiresAuth: true }` 标记需要认证的路由
- 未认证用户自动跳转到登录页

#### 样式规范
- 使用 Tailwind CSS utility classes
- 不使用 scoped CSS 文件
- 图标使用 @heroicons/vue

## 常见问题

### 后端启动失败
- 检查 MySQL 和 Redis 是否正常运行
- 确认数据库配置是否正确
- 查看日志文件定位错误

### 前端连接后端失败
- 确认后端服务是否启动（http://localhost:8080）
- 检查 Token 是否有效
- 查看 Network 面板了解请求详情

### 登录失败
- 确认用户名和密码正确
- 检查密码是否符合格式要求
- 查看后端日志获取详细错误信息

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发送邮件

## 更新日志

### v1.0.0 (2026-01-20)
- ✅ 完成基础后端架构
- ✅ 实现用户认证模块
- ✅ 实现课程管理功能
- ✅ 实现订单管理功能
- ✅ 完成前端 Vue 3 项目
- ✅ 集成管理后台
- ✅ 完善API文档
