# webcam-simulator

Simula una webcam (y opcionalmente un micrófono) en una Raspberry Pi (u otro Linux)
usando `v4l2loopback`: crea un dispositivo virtual `/dev/videoX` y le inyecta un video
en loop, para que cualquier app (Zoom, navegador, OBS, etc.) lo vea como una cámara
real. El audio del mismo archivo se puede loopear por separado hacia un micrófono
virtual.

## Requisitos

- Linux con soporte para módulos del kernel (probado en Raspberry Pi OS).
- Python 3.
- `v4l2loopback-dkms` (lo instala el script de setup de video).
- `ffmpeg` y PulseAudio/PipeWire (lo instala el script de setup de audio).

## Instalación

```bash
# 1. Crear el dispositivo de video virtual (una sola vez; persiste tras reiniciar)
./setup_v4l2loopback.sh [video_nr] [card_label]
# por defecto: video_nr=10 -> /dev/video10, card_label="VirtualCam"

# 2. Crear el micrófono virtual (opcional, solo si también quieres enviar audio)
./setup_audio_loopback.sh [sink_name]
# por defecto: sink_name=VirtualMic

# 3. Entorno Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
# Video
python3 webcam_simulator.py path/al/video.mp4 \
    --device /dev/video10 \
    --width 1280 \
    --height 720 \
    --fps 30

# Audio (en otra terminal, en paralelo, si quieres enviar también el audio)
python3 audio_simulator.py path/al/video.mp4 --sink VirtualMic
```

`webcam_simulator.py` reproduce el video en loop (vuelve al primer frame al llegar al
final) y lo escribe continuamente en el dispositivo indicado. `audio_simulator.py`
usa `ffmpeg` para loopear la pista de audio del mismo archivo hacia el sink virtual;
en tu app de videollamada, selecciona `VirtualCam` como cámara y `VirtualMic Monitor`
(o "Monitor of VirtualMic") como micrófono. Detén cualquiera de los dos con `Ctrl+C`.

### Verificar los dispositivos

```bash
v4l2-ctl --list-devices
ffplay /dev/video10

pactl list short sinks
```

## Archivos

- `setup_v4l2loopback.sh` — instala y carga `v4l2loopback`, dejando el dispositivo
  de video virtual disponible también tras reiniciar.
- `webcam_simulator.py` — abre un video con OpenCV y lo transmite en loop al
  dispositivo virtual usando `pyfakewebcam`.
- `setup_audio_loopback.sh` — instala `ffmpeg`/`pulseaudio-utils` y crea un sink nulo
  (micrófono virtual) vía un servicio de usuario systemd, para que persista entre
  sesiones.
- `audio_simulator.py` — usa `ffmpeg` para loopear la pista de audio de un video hacia
  el sink virtual.
- `requirements.txt` — dependencias de Python (`opencv-python`, `pyfakewebcam`,
  `numpy`).
