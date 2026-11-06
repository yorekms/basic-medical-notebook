#!/usr/bin/env python3
"""Audit and render 60-minute 3-voice 'Basic Medical: Behind the Curtain' podcast episodes.

Supports two synthesis engines out of the box:
  1. `--engine gemini` (`gemini-3.8-flash-tts` via `google-genai >= 2.25.0`):
     - Partitions 3-speaker episodes into 2-speaker `speech_config={"speakers": [...]}` blocks
       and 1-speaker blocks, extracts RIFF-safe PCM frames, and stitches WAV + 192k AAC `.m4a`.
  2. `--engine edge` (Zero-API-key neural `edge-tts` + `imageio-ffmpeg` -> `.m4a`):
     - Renders every turn with its dedicated Microsoft Neural voice, strips inline `<...>` tags,
       concatenates cleanly with natural inter-turn pauses, and outputs Carrd-ready `.m4a` files.

Usage:
  # Audit all 8 marathon scripts (word counts, speaker balance, zero '$'/'\\' check):
  python scripts/render_basic_medical_60min_tts.py --audit-all

  # Audit a single episode offline:
  python scripts/render_basic_medical_60min_tts.py LONGFORM_60MIN_PODCAST_EP801_KIDNEY_DONOR_GAUNTLET_MGFR_24HR_URINE_AND_SPLIT_SCANS.md --dry-run

  # Render full 60-minute 3-voice M4A with zero API keys (Edge Neural TTS):
  python scripts/render_basic_medical_60min_tts.py LONGFORM_60MIN_PODCAST_EP801_KIDNEY_DONOR_GAUNTLET_MGFR_24HR_URINE_AND_SPLIT_SCANS.md --engine edge

  # Render full 60-minute 3-voice WAV + M4A with Gemini 3.8 Flash TTS:
  $env:GEMINI_API_KEY="YOUR_KEY"
  python scripts/render_basic_medical_60min_tts.py LONGFORM_60MIN_PODCAST_EP801_KIDNEY_DONOR_GAUNTLET_MGFR_24HR_URINE_AND_SPLIT_SCANS.md --engine gemini
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import dataclasses
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import time
import wave
from typing import Dict, List, Optional, Tuple


MODEL_ID = "gemini-3.8-flash-tts"

# Clean Carrd-friendly output filenames (no '60m' clutter in audio titles)
CLEAN_AUDIO_STEMS: Dict[str, str] = {
    "EP801": "EP801_Kidney_Donor_Gauntlet_mGFR_Litholink_and_Split_Scans",
    "EP802": "EP802_HLA_Typing_Luminex_Prozone_and_Living_Cell_Crossmatch",
    "EP803": "EP803_Eight_Colored_Tubes_Core_Chemistry_and_Immunoassay_Traps",
    "EP804": "EP804_Behind_the_Lead_Glass_and_the_Frozen_Section_Cryostat",
    "EP805": "EP805_The_Oncology_Workup_Tumor_Markers_Liquid_Biopsy_and_Theranostics",
    "EP806": "EP806_ICU_Red_Alert_Orders_Shock_Gaps_Ventilator_Curves_and_Coma_EEG",
    "EP807": "EP807_From_Womb_to_Heel_Stick_NIPT_Tandem_MS_Sweat_Chloride_and_Trio_Exomes",
    "EP808": "EP808_The_Jeopardy_Grandmaster_Tour_Microbiology_Fluid_Taps_and_Classic_Tests",
}

# Zero-overlap 21-Voice Studio Roster across Cast Modes A-G
SPEAKER_PROFILES: Dict[str, Dict[str, str]] = {
    # Cast Mode A — EP801 & EP802 (Living Kidney Donor & Transplant Immunology)
    "Dr. Rachel Halpern": {
        "gemini_voice": "Sulafat",
        "edge_voice": "en-US-AvaMultilingualNeural",
        "style": "warm, razor-sharp transplant nephrologist and living donor medical director",
    },
    "Prof. Evan Reid": {
        "gemini_voice": "Sadaltager",
        "edge_voice": "en-US-AndrewMultilingualNeural",
        "style": "curious, deeply knowledgeable biophysicist and prospective living kidney donor",
    },
    "Carlos Mendez": {
        "gemini_voice": "Orus",
        "edge_voice": "en-US-BrianMultilingualNeural",
        "style": "hands-on lead LC-MS/MS, nuclear clearance, and HLA histocompatibility technologist",
    },
    # Cast Mode B — EP803 (Phlebotomy, Core Chemistry, Hematology & Immunoassays)
    "Dr. Nathan Sterling": {
        "gemini_voice": "Charon",
        "edge_voice": "en-US-ChristopherNeural",
        "style": "resonant, authoritative director of clinical chemistry and toxicology",
    },
    "Dr. Maya Lin": {
        "gemini_voice": "Zephyr",
        "edge_voice": "en-US-EmmaMultilingualNeural",
        "style": "sharp, inquisitive internal medicine diagnostician and patient advocate",
    },
    "Denise Okafor": {
        "gemini_voice": "Autonoe",
        "edge_voice": "en-GB-SoniaNeural",
        "style": "energetic lead medical laboratory scientist running core automation and mass spec",
    },
    # Cast Mode E — EP804 (Radiology, Nuclear PET, Surgical Pathology & Procedures)
    "Dr. Victor Chen": {
        "gemini_voice": "Iapetus",
        "edge_voice": "en-US-EricNeural",
        "style": "clear, vivid diagnostic radiologist and nuclear medicine physician",
    },
    "Dr. Elena Rostova": {
        "gemini_voice": "Erinome",
        "edge_voice": "en-US-MichelleNeural",
        "style": "articulate surgical pathologist and cardiopulmonary diagnostician",
    },
    "Marcus Bell": {
        "gemini_voice": "Fenrir",
        "edge_voice": "en-US-RogerNeural",
        "style": "seasoned chief CT/MRI technologist and frozen-section histotechnologist",
    },
    # Cast Mode C — EP805 (Oncology, Marrow Flow, NGS, ctDNA & Theranostics)
    "Dr. Julian Vance": {
        "gemini_voice": "Rasalgethi",
        "edge_voice": "en-GB-RyanNeural",
        "style": "measured, authoritative medical oncologist and precision cancer genomics director",
    },
    "Dr. Clara Sterling": {
        "gemini_voice": "Aoede",
        "edge_voice": "en-US-JennyNeural",
        "style": "quick-witted cancer biologist and devil's-advocate interviewer",
    },
    "Tariq Al-Mansoor": {
        "gemini_voice": "Algenib",
        "edge_voice": "en-US-SteffanNeural",
        "style": "veteran hematopathology 10-color flow cytometry, NGS, and theranostics specialist",
    },
    # Cast Mode D — EP806 (ICU, Shock, Ventilator Waveforms, TEG & Neurocritical Care)
    "Dr. Kendra Brooks": {
        "gemini_voice": "Kore",
        "edge_voice": "en-US-AriaNeural",
        "style": "commanding, calm-under-fire shock-trauma and pulmonary critical care intensivist",
    },
    "Sam Callahan": {
        "gemini_voice": "Achird",
        "edge_voice": "en-US-GuyNeural",
        "style": "grounded, quantitative emergency physician challenging every assumption",
    },
    "Hannah Lindqvist": {
        "gemini_voice": "Vindemiatrix",
        "edge_voice": "en-GB-LibbyNeural",
        "style": "composed lead STAT blood-gas, viscoelastic TEG, and ICU coma EEG technologist",
    },
    # Cast Mode F — EP807 (Prenatal NIPT, Newborn Heel-Stick MS/MS, Pediatrics & Trio Genomes)
    "Dr. Priya Nair": {
        "gemini_voice": "Despina",
        "edge_voice": "en-IN-NeerjaNeural",
        "style": "warm, lucid neonatologist, pediatrician, and biochemical medical geneticist",
    },
    "Leo Vance": {
        "gemini_voice": "Puck",
        "edge_voice": "en-AU-WilliamNeural",
        "style": "upbeat, curious new-parent scientist and diagnostic sleuth",
    },
    "Grace Takahashi": {
        "gemini_voice": "Leda",
        "edge_voice": "en-US-AnaNeural",
        "style": "meticulous state newborn-screening tandem mass spec and rapid trio-genome specialist",
    },
    # Cast Mode G — EP808 (Microbiology, Body Taps, Autoimmunity & Jeopardy Grandmaster Tour)
    "Dr. Arthur Pendelton": {
        "gemini_voice": "Gacrux",
        "edge_voice": "en-GB-ThomasNeural",
        "style": "encyclopedic, witty infectious disease and diagnostic grandmaster clinician",
    },
    "Zoe Patel": {
        "gemini_voice": "Callirrhoe",
        "edge_voice": "en-AU-NatashaNeural",
        "style": "sharp, lively chief medical resident and diagnostic trivia challenger",
    },
    "Matteo Rossi": {
        "gemini_voice": "Schedar",
        "edge_voice": "en-IE-ConnorNeural",
        "style": "seasoned clinical MALDI-TOF microbiologist and polarized-light microscopist",
    },
}

ALLOWED_INLINE_TAGS = {
    "<short pause>",
    "<breath>",
    "<sigh>",
    "<laugh>",
    "<cough>",
    "<throat-clearing>",
}

SPEAKER_LINE_RE = re.compile(r"^\*\*\[?([^*\]:]+)\]?:\*\*\s*(.*)$")


@dataclasses.dataclass
class DialogueTurn:
    index: int
    speaker: str
    text: str
    word_count: int


@dataclasses.dataclass
class SynthesisChunk:
    chunk_index: int
    mode: str  # "multi" (2 speakers) or "single" (1 speaker)
    speakers: List[str]
    turns: List[DialogueTurn]

    @property
    def word_count(self) -> int:
        return sum(t.word_count for t in self.turns)


def resolve_ffmpeg() -> Optional[str]:
    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return system_ffmpeg
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def resolve_clean_stem(script_path: pathlib.Path) -> str:
    match = re.search(r"(EP\d{3})", script_path.name)
    if match and match.group(1) in CLEAN_AUDIO_STEMS:
        return CLEAN_AUDIO_STEMS[match.group(1)]
    return re.sub(r"^LONGFORM_60MIN_PODCAST_", "", script_path.stem)


def clean_markdown_for_tts(raw_text: str) -> str:
    protected: Dict[str, str] = {}
    text = raw_text
    for idx, tag in enumerate(ALLOWED_INLINE_TAGS):
        placeholder = f"__VOCAL_TAG_{idx}__"
        if tag in text:
            protected[placeholder] = tag
            text = text.replace(tag, placeholder)

    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = text.replace("`", "")
    text = re.sub(r"\s+", " ", text).strip()

    for placeholder, tag in protected.items():
        text = text.replace(placeholder, tag)
    return text


def strip_inline_tags_for_edge(text: str) -> str:
    cleaned = text
    for tag in ALLOWED_INLINE_TAGS:
        cleaned = cleaned.replace(tag, " ... " if "pause" in tag else " ")
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()


def parse_script(markdown_path: pathlib.Path) -> List[DialogueTurn]:
    lines = markdown_path.read_text(encoding="utf-8").splitlines()
    turns: List[DialogueTurn] = []
    current_speaker: Optional[str] = None
    buffer: List[str] = []

    def flush() -> None:
        nonlocal current_speaker, buffer
        if current_speaker and buffer:
            joined = " ".join(part.strip() for part in buffer if part.strip())
            cleaned = clean_markdown_for_tts(joined)
            if cleaned:
                spoken_only = strip_inline_tags_for_edge(cleaned)
                turns.append(
                    DialogueTurn(
                        index=len(turns) + 1,
                        speaker=current_speaker,
                        text=cleaned,
                        word_count=len(spoken_only.split()),
                    )
                )
        current_speaker = None
        buffer = []

    in_metadata_header = True
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("### ACT ") or stripped.startswith("## ACT "):
            in_metadata_header = False
            flush()
            continue
        if in_metadata_header:
            match_early = SPEAKER_LINE_RE.match(stripped)
            if match_early and match_early.group(1).strip() in SPEAKER_PROFILES:
                in_metadata_header = False
            else:
                continue
        if stripped.startswith("---") or stripped.startswith("#"):
            flush()
            continue

        match = SPEAKER_LINE_RE.match(stripped)
        if match:
            flush()
            current_speaker = match.group(1).strip()
            remainder = match.group(2).strip()
            if remainder:
                buffer.append(remainder)
        elif current_speaker is not None and stripped:
            buffer.append(stripped)

    flush()
    return turns


def build_chunks(turns: List[DialogueTurn], max_words_per_chunk: int = 900) -> List[SynthesisChunk]:
    chunks: List[SynthesisChunk] = []
    active_turns: List[DialogueTurn] = []
    active_speakers: List[str] = []

    def emit_active() -> None:
        nonlocal active_turns, active_speakers
        if not active_turns:
            return
        unique_speakers = list(dict.fromkeys(t.speaker for t in active_turns))
        mode = "single" if len(unique_speakers) == 1 else "multi"
        chunks.append(
            SynthesisChunk(
                chunk_index=len(chunks) + 1,
                mode=mode,
                speakers=unique_speakers,
                turns=active_turns,
            )
        )
        active_turns = []
        active_speakers = []

    for turn in turns:
        prospective_speakers = list(dict.fromkeys(active_speakers + [turn.speaker]))
        current_words = sum(t.word_count for t in active_turns)
        if len(prospective_speakers) > 2 or (
            active_turns and current_words + turn.word_count > max_words_per_chunk
        ):
            emit_active()
        active_turns.append(turn)
        if turn.speaker not in active_speakers:
            active_speakers.append(turn.speaker)

    emit_active()
    return chunks


def resolve_gemini_voice(speaker: str) -> Tuple[str, str]:
    if speaker in SPEAKER_PROFILES:
        p = SPEAKER_PROFILES[speaker]
        return p["gemini_voice"], p["style"]
    return "Sadaltager", "clear, engaging clinical diagnostics podcast host"


def resolve_edge_voice(speaker: str) -> str:
    if speaker in SPEAKER_PROFILES:
        return SPEAKER_PROFILES[speaker]["edge_voice"]
    return "en-US-AndrewMultilingualNeural"


def audit_script(script_path: pathlib.Path, max_words_per_chunk: int = 900) -> Tuple[bool, int, int]:
    turns = parse_script(script_path)
    if not turns:
        print(f"[FAIL] {script_path.name}: 0 dialogue turns parsed!", file=sys.stderr)
        return False, 0, 0

    raw_text = script_path.read_text(encoding="utf-8")
    total_words = sum(t.word_count for t in turns)
    est_minutes = total_words / 145.0
    speakers_seen = list(dict.fromkeys(t.speaker for t in turns))
    stray_dollar = raw_text.count("$")
    stray_backslash = raw_text.count("\\")
    chunks = build_chunks(turns, max_words_per_chunk=max_words_per_chunk)
    unknown_speakers = [s for s in speakers_seen if s not in SPEAKER_PROFILES]

    print(f"=== Audit: {script_path.name} -> {resolve_clean_stem(script_path)}.m4a ===")
    print(f"  Turns            : {len(turns)}")
    print(f"  Spoken Words     : {total_words:,} (~{est_minutes:.1f} min @ 145 wpm)")
    print(f"  Gemini Chunks    : {len(chunks)} ({sum(1 for c in chunks if c.mode == 'multi')} 2-voice, {sum(1 for c in chunks if c.mode == 'single')} 1-voice)")
    print(f"  File '$' / '\\'   : {stray_dollar} / {stray_backslash}")
    for spk in speakers_seen:
        g_voice, _ = resolve_gemini_voice(spk)
        e_voice = resolve_edge_voice(spk)
        spk_words = sum(t.word_count for t in turns if t.speaker == spk)
        spk_turns = sum(1 for t in turns if t.speaker == spk)
        print(f"    * {spk:24s} | Gemini: {g_voice:12s} | Edge: {e_voice:28s} | {spk_turns:2d} turns ({spk_words:,} words)")

    ok = (stray_dollar == 0) and (stray_backslash == 0) and (not unknown_speakers) and (total_words >= 7500)
    if unknown_speakers:
        print(f"  [WARN] Unmapped speakers: {unknown_speakers}", file=sys.stderr)
    if stray_dollar or stray_backslash:
        print("  [WARN] Stray '$' or '\\' found in script!", file=sys.stderr)
    return ok, total_words, len(turns)


def synthesize_gemini_chunk_wav(client, chunk: SynthesisChunk) -> bytes:
    if chunk.mode == "single":
        speaker = chunk.speakers[0]
        voice_name, style = resolve_gemini_voice(speaker)
        combined_text = " ".join(t.text for t in chunk.turns)
        interaction = client.interactions.create(
            model=MODEL_ID,
            input=[
                {
                    "type": "user_input",
                    "content": [
                        {
                            "type": "text",
                            "text": combined_text,
                            "annotations": [{"type": "speech_metadata", "style": style}],
                        }
                    ],
                }
            ],
            response_format={"type": "audio"},
            generation_config={"speech_config": [{"voice": voice_name}]},
        )
        return base64.b64decode(interaction.output_audio.data)

    speakers_cfg = []
    for spk in chunk.speakers:
        voice_name, _ = resolve_gemini_voice(spk)
        speakers_cfg.append({"speaker": spk, "voice": voice_name})

    content_blocks = []
    for turn in chunk.turns:
        _, style = resolve_gemini_voice(turn.speaker)
        content_blocks.append(
            {
                "type": "text",
                "text": turn.text,
                "annotations": [
                    {"type": "speech_metadata", "speaker": turn.speaker, "style": style}
                ],
            }
        )

    interaction = client.interactions.create(
        model=MODEL_ID,
        input=[{"type": "user_input", "content": content_blocks}],
        response_format={"type": "audio"},
        generation_config={"speech_config": {"speakers": speakers_cfg}},
    )
    return base64.b64decode(interaction.output_audio.data)


def stitch_wav_segments(
    segment_files: List[Tuple[pathlib.Path, str]],
    output_wav: pathlib.Path,
    pause_ms: int = 280,
) -> float:
    params = None
    total_frames = 0
    with wave.open(str(output_wav), "wb") as master:
        for idx, (seg_path, _) in enumerate(segment_files):
            with wave.open(str(seg_path), "rb") as reader:
                seg_params = (
                    reader.getnchannels(),
                    reader.getsampwidth(),
                    reader.getframerate(),
                )
                if params is None:
                    params = seg_params
                    master.setnchannels(params[0])
                    master.setsampwidth(params[1])
                    master.setframerate(params[2])
                frames = reader.readframes(reader.getnframes())
                master.writeframes(frames)
                total_frames += reader.getnframes()

            if idx < len(segment_files) - 1 and params is not None:
                silence_frames = int(params[2] * (pause_ms / 1000.0))
                master.writeframes(b"\x00" * (silence_frames * params[0] * params[1]))
                total_frames += silence_frames
    return 0.0 if params is None else total_frames / float(params[2])


async def render_edge_episode(
    turns: List[DialogueTurn],
    output_dir: pathlib.Path,
    clean_stem: str,
) -> pathlib.Path:
    import edge_tts

    ffmpeg_bin = resolve_ffmpeg()
    if not ffmpeg_bin:
        raise RuntimeError("ffmpeg not found on PATH and imageio-ffmpeg is not installed.")

    chunk_dir = output_dir / f"{clean_stem}_edge_turns"
    chunk_dir.mkdir(parents=True, exist_ok=True)
    sem = asyncio.Semaphore(3)

    async def synth_one(turn: DialogueTurn) -> pathlib.Path:
        mp3_path = chunk_dir / f"turn_{turn.index:04d}.mp3"
        if mp3_path.exists() and mp3_path.stat().st_size > 512:
            return mp3_path
        voice = resolve_edge_voice(turn.speaker)
        clean_text = strip_inline_tags_for_edge(turn.text)
        async with sem:
            for attempt in range(4):
                try:
                    comm = edge_tts.Communicate(clean_text, voice)
                    await comm.save(str(mp3_path))
                    if mp3_path.exists() and mp3_path.stat().st_size > 512:
                        return mp3_path
                except Exception as exc:
                    if attempt == 3:
                        raise
                    await asyncio.sleep(1.5 * (attempt + 1))
        return mp3_path

    tasks = [synth_one(t) for t in turns]
    turn_files = await asyncio.gather(*tasks)

    silence_mp3 = chunk_dir / "pause_280ms.mp3"
    if not silence_mp3.exists():
        subprocess.run(
            [
                ffmpeg_bin,
                "-y",
                "-f",
                "lavfi",
                "-i",
                "anullsrc=r=24000:cl=mono",
                "-t",
                "0.28",
                "-q:a",
                "9",
                str(silence_mp3),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    concat_list = chunk_dir / "concat_list.txt"
    lines = []
    for idx, mp3_file in enumerate(turn_files):
        safe_p = str(mp3_file.resolve()).replace("\\", "/")
        lines.append(f"file '{safe_p}'")
        if idx < len(turn_files) - 1:
            safe_s = str(silence_mp3.resolve()).replace("\\", "/")
            lines.append(f"file '{safe_s}'")
    concat_list.write_text("\n".join(lines), encoding="utf-8")

    output_m4a = output_dir / f"{clean_stem}.m4a"
    subprocess.run(
        [
            ffmpeg_bin,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_list),
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            str(output_m4a),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return output_m4a


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit and synthesize 60-minute 3-voice 'Basic Medical: Behind the Curtain' episodes."
    )
    parser.add_argument(
        "script_path",
        nargs="?",
        type=pathlib.Path,
        help="Path to LONGFORM_60MIN_PODCAST_EP*.md",
    )
    parser.add_argument(
        "--audit-all",
        action="store_true",
        help="Audit every LONGFORM_60MIN_PODCAST_EP*.md script in the project root",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate speaker mappings, word count, and TTS hygiene offline",
    )
    parser.add_argument(
        "--engine",
        choices=("gemini", "edge"),
        default="gemini",
        help="TTS engine: 'gemini' (gemini-3.8-flash-tts) or 'edge' (zero-key neural Edge-TTS)",
    )
    parser.add_argument(
        "--output-dir",
        type=pathlib.Path,
        default=pathlib.Path("rendered_audio"),
        help="Output directory for rendered WAV/M4A files",
    )
    parser.add_argument(
        "--max-words-per-chunk",
        type=int,
        default=900,
        help="Max words per 2-speaker Gemini TTS interaction call",
    )
    args = parser.parse_args()

    project_root = pathlib.Path(__file__).resolve().parent.parent

    if args.audit_all:
        scripts = sorted(project_root.glob("LONGFORM_60MIN_PODCAST_EP*.md"))
        if not scripts:
            print(f"No LONGFORM_60MIN_PODCAST_EP*.md scripts found in {project_root}", file=sys.stderr)
            return 1
        all_ok = True
        grand_words = 0
        grand_turns = 0
        for sp in scripts:
            ok, wc, tc = audit_script(sp, max_words_per_chunk=args.max_words_per_chunk)
            all_ok = all_ok and ok
            grand_words += wc
            grand_turns += tc
            print()
        print(
            f"=== GRAND TOTAL ACROSS {len(scripts)} EPISODES: "
            f"{grand_words:,} spoken words (~{grand_words / 145.0:.1f} minutes) | {grand_turns} turns ==="
        )
        return 0 if all_ok else 2

    if args.script_path is None:
        parser.error("Provide a script_path or --audit-all.")

    ok, _, _ = audit_script(args.script_path, max_words_per_chunk=args.max_words_per_chunk)
    if args.dry_run:
        return 0 if ok else 2

    turns = parse_script(args.script_path)
    clean_stem = resolve_clean_stem(args.script_path)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    if args.engine == "edge":
        print(f"Rendering {len(turns)} multi-voice turns via neural Edge-TTS -> {clean_stem}.m4a ...")
        out_m4a = asyncio.run(render_edge_episode(turns, args.output_dir, clean_stem))
        print(f"Completed M4A audio: {out_m4a}")
        return 0

    from google import genai

    client = genai.Client()
    chunks = build_chunks(turns, max_words_per_chunk=args.max_words_per_chunk)
    chunk_dir = args.output_dir / f"{clean_stem}_gemini_chunks"
    chunk_dir.mkdir(parents=True, exist_ok=True)

    rendered_segments: List[Tuple[pathlib.Path, str]] = []
    for chunk in chunks:
        seg_path = chunk_dir / f"chunk_{chunk.chunk_index:03d}_{chunk.mode}.wav"
        if not (seg_path.exists() and seg_path.stat().st_size > 1024):
            print(
                f"[{chunk.chunk_index:02d}/{len(chunks):02d}] Synthesizing {chunk.mode} "
                f"({', '.join(chunk.speakers)} | {chunk.word_count} words)..."
            )
            seg_path.write_bytes(synthesize_gemini_chunk_wav(client, chunk))
            time.sleep(0.4)
        rendered_segments.append((seg_path, chunk.mode))

    master_wav = args.output_dir / f"{clean_stem}.wav"
    dur = stitch_wav_segments(rendered_segments, master_wav)
    print(f"Stitched WAV: {master_wav} ({dur / 60.0:.1f} min)")

    ffmpeg_bin = resolve_ffmpeg()
    if ffmpeg_bin:
        master_m4a = args.output_dir / f"{clean_stem}.m4a"
        subprocess.run(
            [ffmpeg_bin, "-y", "-i", str(master_wav), "-c:a", "aac", "-b:a", "192k", str(master_m4a)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"Exported M4A: {master_m4a}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
