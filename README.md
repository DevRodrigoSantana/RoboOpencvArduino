# RoboOpencvArduino 🤖

Projeto simples de integração entre **OpenCV em Python** e **Arduino** para controle de robô via visão computacional.

---

## 📌 Visão Geral

Este projeto permite controlar um robô (ou qualquer sistema com motores) a partir de comandos enviados por um script em Python, que utiliza **OpenCV** para capturar e processar imagens de uma câmera.

- O **Arduino** recebe comandos via porta serial e move os motores.
- O **computador** executa um script Python que analisa a imagem da webcam e envia comandos conforme a lógica (ex: rastreamento de cor, detecção de movimento etc).

---

## 📁 Estrutura

RoboOpencvArduino/
├── arduino/
│ └── robo_motores.ino # Código para o Arduino
├── python/
│ └── main.py # Script Python com OpenCV
└── README.md # Este arquivo



---

## ⚙️ Requisitos

### Python
- Python 3.7+
- OpenCV
- PySerial

Instale as dependências com:

pip install opencv-python pyserial mediapipe
