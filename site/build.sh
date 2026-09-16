#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_DIR="$ROOT_DIR/.quartz-build"
QUARTZ_COMMIT="3dff48b5df6d84c9544a5ae19c8f2cbb01dc44e5"

rm -rf "$BUILD_DIR"
git clone --filter=blob:none --no-checkout https://github.com/jackyzha0/quartz.git "$BUILD_DIR"
git -C "$BUILD_DIR" checkout "$QUARTZ_COMMIT"

cp "$ROOT_DIR/site/quartz.config.yaml" "$BUILD_DIR/quartz.config.yaml"
mkdir -p "$BUILD_DIR/content"

cp "$ROOT_DIR/README.md" "$BUILD_DIR/content/index.md"
cp "$ROOT_DIR/README.md" "$BUILD_DIR/content/README.md"
cp "$ROOT_DIR/portfolio.md" "$BUILD_DIR/content/portfolio.md"
cp "$ROOT_DIR/tarefas-escritorio.md" "$BUILD_DIR/content/tarefas-escritorio.md"
cp "$ROOT_DIR/CONTEXTO.md" "$BUILD_DIR/content/CONTEXTO.md"
cp -R "$ROOT_DIR/atividades" "$BUILD_DIR/content/atividades"
cp -R "$ROOT_DIR/conselho" "$BUILD_DIR/content/conselho"
cp -R "$ROOT_DIR/modelos" "$BUILD_DIR/content/modelos"
cp -R "$ROOT_DIR/projetos" "$BUILD_DIR/content/projetos"

npm ci --prefix "$BUILD_DIR"
(cd "$BUILD_DIR" && node quartz/bootstrap-cli.mjs build)
