#!/bin/bash

echo "Iniciando SRHP - Sistema de Recomendacao Hierarquica de Produtos"
echo ""

if ! command -v docker &> /dev/null; then
    echo "ERRO: Docker nao esta instalado. Instale o Docker primeiro."
    exit 1
fi

if ! docker compose version &> /dev/null; then
    echo "ERRO: Docker Compose nao esta instalado. Instale o Docker Compose primeiro."
    exit 1
fi

echo "Parando containers existentes..."
docker compose down

echo "Removendo arquivo de banco vazio se existir..."
rm -f srhp.db

echo "Construindo imagem Docker..."
docker compose build

echo "Iniciando aplicacao..."
docker compose up -d

echo ""
echo "Aguardando aplicacao iniciar..."
sleep 10

echo "Copiando banco de dados do container para o host..."
sleep 3
docker compose cp srhp-app:/app/srhp.db ./srhp.db 2>/dev/null && echo "Banco copiado!" || docker compose cp srhp-app:/app/data/srhp.db ./srhp.db 2>/dev/null && echo "Banco copiado de /app/data!" || echo "Aguardando banco ser criado..."
sleep 2
if [ ! -f srhp.db ] || [ ! -s srhp.db ]; then
    docker compose cp srhp-app:/app/srhp.db ./srhp.db 2>/dev/null || docker compose cp srhp-app:/app/data/srhp.db ./srhp.db 2>/dev/null && echo "Banco copiado com sucesso!"
fi

echo ""
echo "Aplicacao iniciada com sucesso!"
echo "Acesse: http://localhost:8000"
echo ""
echo "Comandos uteis:"
echo "   - Ver logs: docker compose logs -f"
echo "   - Parar: docker compose down"
echo "   - Reiniciar: docker compose restart"
echo "   - Popular banco: docker compose exec srhp-app python scripts/populate_db.py"
echo ""
