# Official Python devcontainer image (stable in Codespaces)
FROM mcr.microsoft.com/devcontainers/python:3.11

# Optional: install Tk so `import tkinter` / `import turtle` doesn’t crash.
# Note: Codespaces is headless → no visible windows; for turtle graphics, run locally.
USER root
RUN apt-get update \
 && apt-get install -y --no-install-recommends python3-tk tk \
 && rm -rf /var/lib/apt/lists/*

# Standard workspace path in Codespaces
WORKDIR /workspaces/PizzaRP
