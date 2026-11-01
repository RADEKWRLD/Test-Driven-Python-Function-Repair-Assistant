ARG BASE_IMAGE=python:3.12-slim
FROM ${BASE_IMAGE}

ARG DEBIAN_FRONTEND=noninteractive
ARG SKIP_APT=0

RUN set -eux; \
    if [ "$SKIP_APT" = "0" ]; then \
        sed -i 's|http://deb.debian.org|https://deb.debian.org|g' \
            /etc/apt/sources.list.d/debian.sources; \
        apt-get update; \
        apt-get install --yes --no-install-recommends bash coreutils git patch ripgrep; \
        rm -rf /var/lib/apt/lists/*; \
    fi; \
    python -m pip install --no-cache-dir "pytest>=8.3,<9" "numpy>=2,<3"

WORKDIR /workspace

# Runtime code adds: --network none, --read-only, a tmpfs /tmp, capability
# dropping, no-new-privileges, resource limits, and only explicit mounts.
CMD ["sleep", "infinity"]
