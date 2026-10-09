# Transcricao de reunioes

Projeto para transcrever arquivos de audio e video localmente usando o OpenAI Whisper. O resultado e salvo em Markdown, com timestamps por segmento.

## Requisitos

- Python instalado e disponivel no terminal
- Conexao com a internet na primeira execucao, para baixar o modelo Whisper escolhido

O `imageio-ffmpeg` fornece o executavel FFmpeg usado para ler audio e video, sem exigir uma instalacao separada do FFmpeg no sistema.

## Instalacao no Windows

No terminal, dentro desta pasta, crie o ambiente virtual e instale as dependencias:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Para ativar o ambiente no PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Para ativar o ambiente no Git Bash (Windows):

```bash
source .venv/Scripts/activate
```

O ambiente `.venv` e local e esta excluido do Git. Repita esses comandos depois de clonar ou copiar o projeto.

## Instalacao no Linux (Bash)

Garanta que Python 3 e o suporte a ambientes virtuais estejam instalados. Em distribuicoes Debian ou Ubuntu, use:

```bash
sudo apt update
sudo apt install python3 python3-venv
```

No terminal, dentro desta pasta, crie o ambiente virtual e instale as dependencias:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
```

Para ativar o ambiente no Bash:

```bash
source .venv/bin/activate
```

O ambiente `.venv` e local e esta excluido do Git. Repita esses comandos depois de clonar ou copiar o projeto.

## Uso

No Windows (PowerShell):

```powershell
.\.venv\Scripts\python.exe transcribe.py "videos\reuniao.mp4" --model medium --lang pt --output "transcriptions\reuniao.md"
```

No Linux (Bash):

```bash
.venv/bin/python transcribe.py "videos/reuniao.mp4" --model medium --lang pt --output "transcriptions/reuniao.md"
```

Argumentos:

- `video`: caminho para o arquivo de audio ou video (obrigatorio)
- `--model`: modelo Whisper (`tiny`, `base`, `small`, `medium` ou `large`); o padrao e `small`
- `--lang`: idioma, por exemplo `pt` ou `en`; se omitido, o Whisper tenta detectar automaticamente
- `--output`: caminho do Markdown de saida; se omitido, usa o caminho do arquivo de entrada com extensao `.md`

A pasta informada em `--output` precisa existir antes da execucao. Modelos maiores podem levar mais tempo e consumir mais memoria; o modelo e baixado na primeira vez que for usado.

## Estrutura

```text
whisper/
|-- transcribe.py
|-- requirements.txt
|-- README.md
|-- videos/          # arquivos de entrada
|-- transcriptions/  # transcricoes geradas
```

Os diretorios `videos/` e `transcriptions/` sao locais de trabalho; crie-os novamente caso nao estejam presentes no clone do repositorio.