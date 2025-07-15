# 🛠 Week 6 Guided Lab — Containers & Docker

## 🔍 5W1H: Why This Lab?

- **Who**: You, as the DevOps engineer preparing app containers for staging/prod.
- **What**: Build, run, scan, and ship containers.
- **When**: Every deploy cycle.
- **Where**: Local dev → CI/CD → prod orchestrator.
- **Why**: Portability, consistency, security.
- **How**: Practice these steps.

---

## 📌 Prerequisites

- Docker Desktop or Docker CLI installed.
- Sample app build output (e.g., from Week 4).

---

## 1️⃣ Build a Basic Docker Image

✅ Create `Dockerfile`:
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY . .
RUN npm install
CMD ["node", "index.js"]

✅ Build & run:
docker build -t myapp:1.0 .
docker run -p 3000:3000 myapp:1.0

2️⃣ Advanced: Multi-Stage Build
✅ Example for Java:
# Stage 1: Builder
FROM maven:3.9 AS builder
WORKDIR /app
COPY . .
RUN mvn clean package

# Stage 2: Runtime
FROM openjdk:17-jdk-slim
WORKDIR /app
COPY --from=builder /app/target/app.jar /app/app.jar
ENTRYPOINT ["java", "-jar", "/app/app.jar"]

✅ Build & run:
docker build -t myapp:2.0 .
docker run -p 8080:8080 myapp:2.0

3️⃣ Docker Compose (Multi-Container Dev)
✅ Create docker-compose.yml:

version: "3.9"
services:
  app:
    build: .
    ports:
      - "3000:3000"
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypass

✅ Start:
docker-compose up -d
docker-compose ps

4️⃣ Scan & Sign
✅ Scan image for vulnerabilities:
docker scan myapp:2.0
# or use Trivy
trivy image myapp:2.0

✅ Sign image:
cosign sign --key cosign.key myapp:2.0

✅ Verify:
cosign verify --key cosign.pub myapp:2.0

5️⃣ Push to Registry
✅ Tag & push:
docker tag myapp:2.0 yourdockerhub/myapp:2.0
docker push yourdockerhub/myapp:2.0

✅ Use secrets properly:
Never bake secrets in the image.
Use env vars or secret managers at runtime.

✅ Deliverables
Dockerfile (multi-stage if possible)
docker-compose.yml for local dev
scan-results.md with vulnerabilities found
Image pushed to your registry