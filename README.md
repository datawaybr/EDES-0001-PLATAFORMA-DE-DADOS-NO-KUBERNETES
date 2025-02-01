# DataWay BR
# Kubernetes - Gerenciando Plataformas de Dados no Kubernetes

## Contexto
Através do Kubernetes é possível gerenciar aplicações e processos de maneira distribuída e segmentada. Onde dentro de cada aplicação é possível visualizar e governar cada conjunto do todo.

Apesar do Kubernetes ter seu dia a dia mais nas grandes nuvens (Azure, Aws e Google). É possível ter um cluster pra chamar de seu na sua própria máquina.

Neste projeto vamos fazer passo a passo:
- Configurar e iniciar um cluster de nó único no Minikube;
- Configurar uma aplicação que irá gerenciar as nossas aplicações sozinha;
- Configurar o MinIO;
- Configurar um ambiente de Desenvolvimento pronto com PySpark integrado;
- Configurar um operador que gerencia as aplicações spark;
- Configurar um ambiente de monitoramento com métricas e dashboards;
- Configurar uma ferramenta que calcula os custos do ambiente;
- Configurar uma ferramenta de orquestração dos processos executados.

## Escopo
![Alt text](/docs/fluxogramas/Introducao_Arquitetura.png "Introdução a Arquitetura")

## Pré-Requisitos
Computador Utilizado: Windows 11 + WSL

- Chocolatey
- Docker
- MiniKube
- Helm Chart
- Git
- Poetry

## Ferramentas
- Minikube
- Docker
- ArgoCD
- MinIO
- Airflow
- Kube-Prometheus-Stack (Prometheus + Grafana)
- PySpark
- KubeCost

## Documentações
- [Link das Documentações em Fluxograma](docs/fluxogramas/)
- [Link das Documentações Escritas](docs/pdfs-modulos/)

## Observações
- A stack bem como as versões de todas as ferramentas foi testada em ambiente Minikube.
- Caso a stack seja utilizada em ambiente cloud (AWS, Azure ou GCP) podem ocorrer algumas incoerências durante o deploy das ferramentas abaixo:
    - Prometheus Operator
    - KubeCost
    - ServiceMonitor
    - PodMonitor
    - SparkOperator com CDR's de PodMonitor
- Para abrir os arquivos .excalidraw é necessário baixar a extensão do Excalidraw no VSCode. Ao exportar os fluxos para imagem algumas caixinhas acabem quebrando os links.