FROM python:3.12-slim AS base

# Security: run as non-root user
RUN groupadd -r gitpilot && useradd -r -g gitpilot -m gitpilot

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent files
COPY agent.yaml SOUL.md RULES.md ./
COPY skills/ ./skills/
COPY tools/ ./tools/
COPY .gitclaw/ ./.gitclaw/
COPY .clawless/ ./.clawless/
COPY .gitpilot/ ./.gitpilot/

# Create audit & cache directories
RUN mkdir -p .gitpilot/audit .gitpilot/cache .gitpilot/logs && \
    chown -R gitpilot:gitpilot /app

# Switch to non-root user
USER gitpilot

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:8090/api/v1/health || exit 1

EXPOSE 8090

# Default: run clawless standalone server
CMD ["clawless", "serve", "--config", ".clawless/config.yaml"]
