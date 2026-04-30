# DevOps Examples

This repository section contains infrastructure, containerization, and CI/CD examples reflecting best practices for modern software delivery. As a Sysadmin and DevOps engineer, these configurations prioritize security, high availability (HA), predictability, and observability.

## Directory Structure

* **`ci-cd/`**: Examples of automated pipelines.
  * **`github-actions/`**: Workflows for validating, building, and deploying the frontend (Astro) and backend (Python/FastAPI).
  * **`gitlab-ci/`**: An equivalent pipeline for environments relying on GitLab.
* **`docker/`**: Containerization examples.
  * **`Dockerfile.multi-stage`**: A production-ready multi-stage build for a Python application using `uv`.
  * **`docker-compose.dev.yml`**: A local development environment scaffolding dependencies like PostgreSQL and Redis.
* **`kubernetes/`**: Kubernetes manifests following a base/overlay structure using Kustomize. Features include resource limits, liveness/readiness probes, and proper routing.
* **`observability/`**: An out-of-the-box local monitoring stack using Prometheus and Grafana, pre-provisioned via Docker Compose.

## Principles Followed

1. **Infrastructure as Code (IaC):** Everything is declared via code, ensuring reproducibility.
2. **Shift-Left Security:** CI/CD pipelines include linting and static analysis early in the process.
3. **Observability First:** Standardized metrics exposition to visualize system health immediately.
4. **Clean Architecture compatibility:** Container builds and deployments respect the separation of concerns present in the application's source code.
