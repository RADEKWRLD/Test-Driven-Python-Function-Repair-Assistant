FROM python:3.12-slim

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install --yes --no-install-recommends bash coreutils git patch ripgrep \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --no-cache-dir "pytest>=8.3,<9"

WORKDIR /workspace

# Runtime code adds: --network none, --read-only, a tmpfs /tmp, capability
# dropping, no-new-privileges, resource limits, and only explicit mounts.
CMD ["sleep", "infinity"]
