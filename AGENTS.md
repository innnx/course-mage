# AGENTS.md

This document provides guidelines for agentic coding agents working in this repository.

## Project Overview

Full-stack course management system with Spring Boot 3.2.0 backend (Java 17) and Vue 3 frontend. Uses MySQL for data storage, Redis for caching, JWT for authentication, and MyBatis-Plus for database operations.

---

## Build Commands

### Backend (Maven)
```bash
# Clean and build
mvn clean package

# Run application
mvn spring-boot:run

# Run all tests
mvn test

# Run a single test class
mvn test -Dtest=ClassName

# Run a single test method
mvn test -Dtest=ClassName#methodName

# Skip tests during build
mvn clean package -DskipTests
```

### Frontend (Vite)
```bash
cd frontend-vue

# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## Java Code Style

### Imports
- Use standard Java import ordering: `java.*`, `jakarta.*`, `org.*`, `com.*`
- No wildcard imports (e.g., avoid `import java.util.*`)

### Annotations
- Use Lombok `@RequiredArgsConstructor` for constructor injection instead of `@Autowired`
- Use `@Slf4j` for logging
- Use `@Data` on entities/DTOs
- Use Spring validation annotations (`@NotNull`, `@NotBlank`, `@Size`) on DTOs
- Use `@Tag` and `@Operation` (OpenAPI/Swagger) on controllers

### Controllers
```java
@Tag(name = "Description")
@RestController
@RequestMapping("/api/resource")
@RequiredArgsConstructor
public class ResourceController {
    private final ResourceService resourceService;

    @Operation(summary = "Description")
    @PostMapping
    public Result<Void> create(@Valid @RequestBody RequestDto request) {
        resourceService.create(request);
        return Result.success();
    }
}
```

### Services
- Use interface + implementation pattern
- Use `@Service` on implementation classes
- Throw `BusinessException` for business logic errors
- Use `LambdaQueryWrapper` for MyBatis-Plus queries
- Add `@Slf4j` and log important operations

### Entities
- Use `@Data` from Lombok
- Use `@TableName("table_name")` for table mapping
- Use `@TableId(type = IdType.AUTO)` for primary keys
- Use `@TableLogic` for soft delete fields
- Use `@TableField(fill = FieldFill.INSERT/INSERT_UPDATE)` for timestamps

### Mappers
- Extend `BaseMapper<Entity>`
- No custom SQL in mapper interfaces (use XML files only if needed)

### Result Wrapper
Always return `Result<T>` with code/message/data structure:
```java
Result.success()          // Code 200
Result.success(data)     // Code 200 with data
Result.error(message)     // Code 500
Result.error(code, message)
```

### Exception Handling
- Throw `BusinessException` for business errors:
  ```java
  throw new BusinessException("Error message");
  throw new BusinessException(400, "Custom code");
  ```

### Testing
- Extend `BaseTest` for Spring Boot integration tests
- Use `@Transactional` for auto-rollback after tests
- Use `@BeforeEach`/`@AfterEach` for setup/teardown
- Use `@DisplayName` on test classes and methods
- Use JUnit 5 assertions (`assertNotNull`, `assertEquals`, `assertThrows`)
- Create test data in setup, clean up in teardown

### Naming Conventions
- Classes: PascalCase (e.g., `CourseService`, `CourseController`)
- Methods: camelCase, descriptive verbs (e.g., `createCourse`, `getById`)
- Variables: camelCase
- Constants: UPPER_SNAKE_CASE
- Database tables: snake_case
- API endpoints: kebab-case for resources, camelCase for query params

### Security
- Use `SecurityUtils.getCurrentUsrId()` to get authenticated user ID
- Add `@PreAuthorize` for role-based access control if needed
- JWT tokens stored in `Authorization: Bearer <token>` header

---

## Frontend Code Style

### Vue Components
- Use Composition API with `<script setup>` syntax
- Use `ref` and `reactive` from Vue
- Use Pinia stores for state management

### API Services
- All API calls centralized in `frontend-vue/src/api/services.js`
- Use axios interceptors for automatic token injection and error handling
- API interceptor automatically returns `response.data.data` on success

### Router
- Define routes in `frontend-vue/src/router/index.js`
- Use `meta: { requiresAuth: true }` for protected routes
- Navigation guards redirect to `/login` if unauthenticated

### Styling
- Use Tailwind CSS utility classes
- No component-scoped CSS files (use Tailwind)
- Use @heroicons/vue for icons

### File Organization
```
frontend-vue/src/
├── api/         # API service calls
├── components/  # Reusable components
├── router/      # Route definitions
├── stores/      # Pinia stores
├── views/       # Page components
├── main.js      # App entry point
└── App.vue      # Root component
```

---

## API Documentation

- Swagger UI available at: http://localhost:8080/swagger-ui.html
- OpenAPI JSON: http://localhost:8080/v3/api-docs
- Use `@Operation` and `@Tag` annotations to document endpoints

---

## Database

- MySQL on port 3306 (use docker-compose or local)
- Database name: `course_db`
- Use MyBatis-Plus for all database operations
- Logical delete enabled (deleted field: 0=active, 1=deleted)

---

## Redis

- Used for caching (session storage, etc.)
- Configured in `src/main/resources/application.yml`

---

## Docker Deployment

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

---

## Common Patterns

### Pagination
Use MyBatis-Plus `Page` object:
```java
Page<CourseVo> page = courseService.queryCourses(request);
return Result.success(page);
```

### Date/Time
Use `LocalDateTime` from `java.time`
- Jackson configured for format: `yyyy-MM-dd HH:mm:ss`
- Timezone: GMT+8 (Asia/Shanghai)

### Decimal Values
Use `BigDecimal` for all monetary values and precise calculations

### Validation
Add validation annotations to DTOs:
```java
@NotBlank(message = "Title required")
@Size(max = 100, message = "Max 100 characters")
private String title;

@NotNull(message = "Price required")
@DecimalMin(value = "0.00", message = "Cannot be negative")
private BigDecimal price;
```

---

## Testing Checklist

After making changes:
1. Run backend tests: `mvn test`
2. Build frontend: `cd frontend-vue && npm run build`
3. Verify Swagger docs load correctly
4. Test affected endpoints manually or via Swagger UI

## Important Notes

- Backend runs on port 8080
- Frontend dev server proxies `/api` to `http://localhost:8080`
- No TypeScript in frontend (plain JavaScript)
- No ESLint/Prettier configured in frontend
- No dedicated lint command in Maven (ensure clean compilation)
