"""
transcribe.py — Transcreve vídeos de planejamento usando OpenAI Whisper (local).

Uso:
    python transcribe.py <video_ou_audio> [--model tiny|base|small|medium|large] [--lang pt]

Saída:
    <arquivo>.md  — transcrição em Markdown com timestamps, pronta para enviar a uma IA.
"""
#python transcribe.py videos/reuniao-x.mp4 --model medium --lang pt --output transcriptions/reuniao-x.md

import sys
import argparse
import logging
from pathlib import Path
from datetime import timedelta

import imageio_ffmpeg
import whisper
import whisper.audio as _whisper_audio

# Whisper chama "ffmpeg" hardcoded; substitui pelo executável do imageio-ffmpeg
_ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
_original_load_audio = _whisper_audio.load_audio


def _patched_load_audio(file, sr=_whisper_audio.SAMPLE_RATE):
    import numpy as np
    from subprocess import run

    cmd = [
        _ffmpeg_exe,
        "-nostdin",
        "-threads", "0",
        "-i", file,
        "-f", "s16le",
        "-ac", "1",
        "-acodec", "pcm_s16le",
        "-ar", str(sr),
        "-",
    ]
    proc = run(cmd, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"ffmpeg falhou (código {proc.returncode}):\n"
            + proc.stderr.decode("utf-8", errors="replace")
        )
    out = proc.stdout
    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0


_whisper_audio.load_audio = _patched_load_audio

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def format_ts(seconds: float) -> str:
    td = timedelta(seconds=int(seconds))
    hours, remainder = divmod(td.seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if td.seconds >= 3600:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def transcribe(video_path: Path, model_name: str, language: str | None) -> str:
    log.info("Carregando modelo Whisper '%s'...", model_name)
    model = whisper.load_model(model_name)

    log.info("Transcrevendo: %s", video_path)
    result = model.transcribe(
        str(video_path),
        language=language,
        verbose=False,
        word_timestamps=False,
    )

    detected_lang = result.get("language", "?")
    log.info("Idioma detectado: %s", detected_lang)

    lines = []
    lines.append(f"# Transcrição — {video_path.name}")
    lines.append(f"\n**Arquivo:** `{video_path}`  ")
    lines.append(f"**Modelo:** `{model_name}`  ")
    lines.append(f"**Idioma detectado:** `{detected_lang}`\n")
    lines.append("---\n")

    for seg in result.get("segments", []):
        ts = format_ts(seg["start"])
        text = seg["text"].strip()
        lines.append(f"**[{ts}]** {text}\n")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Transcreve vídeo com Whisper.")
    parser.add_argument("video", help="Caminho do arquivo de vídeo ou áudio.")
    parser.add_argument(
        "--model",
        default="small",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Modelo Whisper a usar (padrão: small).",
    )
    parser.add_argument(
        "--lang",
        default=None,
        help="Força idioma (ex: pt, en). Se omitido, Whisper detecta automaticamente.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Arquivo de saída .md. Padrão: mesmo nome do vídeo com extensão .md.",
    )
    args = parser.parse_args()

    video_path = Path(args.video)
    if not video_path.exists():
        log.error("Arquivo não encontrado: %s", video_path)
        sys.exit(1)

    output_path = Path(args.output) if args.output else video_path.with_suffix(".md")

    markdown = transcribe(video_path, model_name=args.model, language=args.lang)

    output_path.write_text(markdown, encoding="utf-8")
    log.info("Transcrição salva em: %s", output_path)
    print(f"\nArquivo gerado: {output_path}")


if __name__ == "__main__":
    main()
