– Secure Container CI/CD Pipelines (GitLab, GitHub, AWS)
🧠 Objective
You’ll build two CI/CD pipelines (GitHub Actions & GitLab CI) to:

✅ Build hardened Docker images
✅ Scan them for vulnerabilities (Trivy)
✅ Sign them with cosign
✅ Push them to a secure registry (GitHub Container Registry or GitLab Registry)
✅ Gate deployment using security checks

You’ll also preview integration with AWS CodePipeline (coming up in Challenge Lab & Week 5).

🧱 Project Structure Reminder
notestream/
├── frontend/
│   ├── Dockerfile
│   └── index.js
├── backend/
│   ├── Dockerfile
│   └── app.py
├── .github/
│   └── workflows/
│       └── docker-secure.yml   👈 GitHub Actions
├── .gitlab-ci.yml              👈 GitLab CI/CD
🔐 Pre-Setup: Secrets
For both pipelines, set these secrets:

Key	Value	Where
REGISTRY_USER	GitHub/GitLab username or AWS IAM user	GitHub/GitLab/AWS
REGISTRY_TOKEN	PAT, GitLab token, or AWS secret	GitHub/GitLab/AWS
COSIGN_PASSWORD	Password for cosign.key	GitHub/GitLab
🔁 GitHub Actions CI/CD
📄 .github/workflows/docker-secure.yml
name: Secure Docker CI/CD

on:
  push:
    branches: [main]
  pull_request:

jobs:
  build-scan-sign-push:
    runs-on: ubuntu-latest
    env:
      IMAGE_NAME: ghcr.io/${{ github.repository }}/backend
    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Log in to GHCR
      run: echo "${{ secrets.REGISTRY_TOKEN }}" | docker login ghcr.io -u ${{ secrets.REGISTRY_USER }} --password-stdin

    - name: Build Docker Image
      run: |
        docker build -t $IMAGE_NAME:latest ./backend

    - name: Scan with Trivy
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: ${{ env.IMAGE_NAME }}:latest
        format: table
        exit-code: 1
        severity: CRITICAL,HIGH

    - name: Install Cosign
      uses: sigstore/cosign-installer@v3

    - name: Sign Image
      run: |
        echo "${{ secrets.COSIGN_PASSWORD }}" | cosign sign --key cosign.key $IMAGE_NAME:latest

    - name: Push Image
      run: docker push $IMAGE_NAME:latest
✅ This pipeline:

Blocks pushes with critical/high CVEs

Signs the image before pushing

Uses GitHub Container Registry (you can switch to ECR later)

🦊 GitLab CI/CD
📄 .gitlab-ci.yml
stages:
  - build
  - scan
  - sign
  - push

variables:
  IMAGE_NAME: registry.gitlab.com/$CI_PROJECT_PATH/backend

before_script:
  - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" $CI_REGISTRY

build:
  stage: build
  script:
    - docker build -t $IMAGE_NAME:latest ./backend

scan:
  stage: scan
  image: aquasec/trivy:latest
  script:
    - trivy image --exit-code 1 --severity CRITICAL,HIGH $IMAGE_NAME:latest

sign:
  stage: sign
  image: ghcr.io/sigstore/cosign
  script:
    - echo "$COSIGN_PASSWORD" | cosign sign --key cosign.key $IMAGE_NAME:latest

push:
  stage: push
  script:
    - docker push $IMAGE_NAME:latest
✅ Same pipeline stages, but runs natively in GitLab. Can be extended with:

Dependency scanning

SBOM artifact upload

Release tagging

🛠️ Bonus: SBOM Generation (Optional)
Add this to either pipeline:

- name: Generate SBOM with Syft
  uses: anchore/sbom-action@v0
  with:
    image: $IMAGE_NAME:latest
📦 Registry Options
Option	Pros
GitHub Container Registry	Native to GitHub, supports private repos, cosign-compatible
GitLab Container Registry	Integrated with GitLab runners, fine-grained permissions
AWS ECR (coming next)	Secure IAM-based access, ECS integration, lifecycle rules
✅ What You Now Have
A fully automated, security-gated CI/CD pipeline

Automatic image scanning, signing, and pushing

Secure image delivery for container orchestrators

🔜 Next:

ChallengeLab.md: Break the pipeline with a CVE, fix it, then test signing enforcement

Security.md: CI/CD attack surfaces and pipeline protection

Reflection.md: CI/CD as Policy-as-Code and Gatekeeper

Would you like to continue with the Challenge Lab?

You said:
Yes
ChatGPT said:
Perfect — let's dive into the Week 4 Challenge Lab, where we simulate real-world CI/CD failures and implement secure fixes.