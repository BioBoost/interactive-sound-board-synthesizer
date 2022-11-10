# sound board interactive audio

## installation & setup

### install synthesizer
`bash
python3 -m pip install synthesizer
`

### install audio package
`bash
apt install portaudio19-dev
pip install pyaudio
`

### install mqtt
`bash
pip install paho-mqtt
`
### before starting

```text
pulseaudio -k
pulseaudio -D
```