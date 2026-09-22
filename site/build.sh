#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_DIR="$ROOT_DIR/.quartz-build"
QUARTZ_COMMIT="3dff48b5df6d84c9544a5ae19c8f2cbb01dc44e5"
PORTFOLIO="${PORTFOLIO:-saerj}"
PORTFOLIO_DIR="$ROOT_DIR/portfolios/$PORTFOLIO"

if [[ ! "$PORTFOLIO" =~ ^[a-z0-9][a-z0-9-]*$ ]] || [[ ! -f "$PORTFOLIO_DIR/portfolio.md" ]]; then
  echo "Portfólio inválido ou inexistente: $PORTFOLIO" >&2
  exit 1
fi

rm -rf "$BUILD_DIR"
git clone --filter=blob:none --no-checkout https://github.com/jackyzha0/quartz.git "$BUILD_DIR"
git -C "$BUILD_DIR" checkout "$QUARTZ_COMMIT"

cp "$ROOT_DIR/site/quartz.config.yaml" "$BUILD_DIR/quartz.config.yaml"
mkdir -p "$BUILD_DIR/content"

cp "$PORTFOLIO_DIR/portfolio.md" "$BUILD_DIR/content/index.md"
cp "$PORTFOLIO_DIR/portfolio.md" "$BUILD_DIR/content/README.md"
cp "$PORTFOLIO_DIR/portfolio.md" "$BUILD_DIR/content/portfolio.md"
mkdir -p "$BUILD_DIR/content/conselho"
cp "$ROOT_DIR/conselho/README.md" "$BUILD_DIR/content/conselho/README.md"
cp "$ROOT_DIR/conselho/papeis.md" "$BUILD_DIR/content/conselho/papeis.md"
cp "$ROOT_DIR/conselho/protocolo.md" "$BUILD_DIR/content/conselho/protocolo.md"
cp "$ROOT_DIR/conselho/regras.md" "$BUILD_DIR/content/conselho/regras.md"
mkdir -p "$BUILD_DIR/content/conselho/ideias"
cp "$ROOT_DIR/conselho/ideias/README.md" "$BUILD_DIR/content/conselho/ideias/README.md"
cp -R "$ROOT_DIR/modelos" "$BUILD_DIR/content/modelos"
mkdir -p "$BUILD_DIR/content/portfolios/$PORTFOLIO"
cp "$PORTFOLIO_DIR/portfolio.md" "$BUILD_DIR/content/portfolios/$PORTFOLIO/portfolio.md"
cp -R "$PORTFOLIO_DIR/projetos" "$BUILD_DIR/content/portfolios/$PORTFOLIO/projetos"
cp -R "$PORTFOLIO_DIR/projetos" "$BUILD_DIR/content/projetos"

if [[ "$PORTFOLIO" == "saerj" ]]; then
  cp "$ROOT_DIR/tarefas-escritorio.md" "$BUILD_DIR/content/tarefas-escritorio.md"
  cp -R "$ROOT_DIR/atividades" "$BUILD_DIR/content/atividades"
fi

npm ci --prefix "$BUILD_DIR"
(cd "$BUILD_DIR" && node quartz/bootstrap-cli.mjs build)
