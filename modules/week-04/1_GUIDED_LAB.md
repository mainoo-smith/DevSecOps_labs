# 🛠 Week 4 Guided Lab — Building & Pushing Artifacts (Advanced)

## 🔍 5W1H: Why This Lab?

- **Who**: Acting as a DevOps engineer on a real microservices team.
- **What**: Automate builds, ensure reproducibility, and secure supply chain.
- **When**: Every build you intend to ship to staging/production.
- **Where**: Local → CI/CD → Artifact Repo.
- **Why**: Reliable, repeatable builds protect against “it works on my machine”.
- **How**: Build, test, sign, multi-stage Docker build, and push.

---

## 📌 Prerequisites

- Maven or npm installed.
- Docker installed for multi-stage build.
- Local Nexus/Artifactory or cloud artifact repo access.

---

## 1️⃣ Standard Build & Push

✅ **Basic**:
- Use Maven to compile & package a simple Java API.
- Or npm to build a simple Node.js/React frontend.

✅ **Push**:
- Use Nexus CLI or curl to upload `.jar` or `.tgz`.

---

## 2️⃣ Advanced: Multi-Stage Build (Docker)

- Write a `Dockerfile` that uses a builder image, then copies final output.

```dockerfile
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
```

✅ Build the image:
```bash
docker build -t myapp:1.0 .
```

---

## 3️⃣ Signed Artifacts & Checksums

- Sign your Maven artifacts with GPG.
- Verify integrity:
```bash
sha256sum target/app.jar
```

- Store checksums in your repo: `checksums.txt`.

---

## 4️⃣ Promotion Workflow

- Document how you promote artifacts from dev → staging → prod without rebuilding.
- Use Nexus Staging and `build-notes.md` to outline your process.

---

## 5️⃣ Build Caching

- Test with local Maven `.m2` cache vs. cold build.
- Document speed difference in `week4/cache-results.md`.

---

## ✅ Deliverables

- Signed, versioned artifact pushed to Nexus.
- Multi-stage Dockerfile in your repo.
- `build-notes.md` with signing & checksum details.
- Promotion workflow documented.

---

## 🗝️ Real Project Context

This artifact will be pulled by your CI/CD pipeline in Week 5–7 to build containers and deploy to your Kubernetes cluster.  
A broken or unsigned artifact here could compromise your whole supply chain.

## Analogy

Think of your build process like a secured kitchen with a chef who labels, seals, and logs every dish before it goes out for delivery.