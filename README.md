# webcam-simulator

Simula una webcam en una Raspberry Pi (u otro Linux) usando `v4l2loopback`: crea un
dispositivo virtual `/dev/videoX` y le inyecta un video en loop, para que cualquier
app (Zoom, navegador, OBS, etc.) lo vea como una cámara real.

## Requisitos

- Linux con soporte para módulos del kernel (probado en Raspberry Pi OS).
- Python 3.
- `v4l2loopback-dkms` (lo instala el script de setup).

## Instalación

```bash
# 1. Crear el dispositivo virtual (una sola vez, o tras cada reinicio si no persiste)
./setup_v4l2loopback.sh [video_nr] [card_label]
# por defecto: video_nr=10 -> /dev/video10, card_label="VirtualCam"

# 2. Entorno Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
python3 webcam_simulator.py path/al/video.mp4 \
    --device /dev/video10 \
    --width 1280 \
    --height 720 \
    --fps 30
```

El script reproduce el video en loop (vuelve al primer frame al llegar al final) y lo
escribe continuamente en el dispositivo indicado. Detenlo con `Ctrl+C`.

### Verificar el dispositivo

```bash
v4l2-ctl --list-devices
ffplay /dev/video10
```

## Archivos

- `setup_v4l2loopback.sh` — instala y carga `v4l2loopback`, dejando el dispositivo
  virtual disponible también tras reiniciar.
- `webcam_simulator.py` — abre un video con OpenCV y lo transmite en loop al
  dispositivo virtual usando `pyfakewebcam`.
- `requirements.txt` — dependencias de Python (`opencv-python`, `pyfakewebcam`,
  `numpy`).
