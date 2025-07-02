import cv2
import mediapipe as mp
import serial
import time

# Inicialização do MediaPipe
mp_maos = mp.solutions.hands
maos = mp_maos.Hands()
desenho = mp.solutions.drawing_utils

# Configuração da porta serial
porta_serial = "COM22"  # Altere para a COM correta do seu Arduino
velocidade = 9600
arduino = serial.Serial(porta_serial, velocidade)
time.sleep(2)


# Função para detectar se a mão está fechada (para controlar o 3º servo)
def mao_esta_fechada(pontos_mao):
    dedos = [(8, 6), (12, 10), (16, 14), (20, 18)]
    dedos_fechados = 0
    for ponta, articulacao in dedos:
        if pontos_mao.landmark[ponta].y > pontos_mao.landmark[articulacao].y:
            dedos_fechados += 1
    return dedos_fechados >= 3


# Envia os três valores para o Arduino
def mover_servos(angulo_x, angulo_y, estado_mao_esquerda):
    comando = f"{angulo_x},{angulo_y},{estado_mao_esquerda}\n"
    print(f"Enviando comando: {comando.strip()}")
    arduino.write(comando.encode())


# Inicia a webcam
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)

# Variável para guardar o estado da mão esquerda
estado_mao_esquerda = 1  # padrão: aberta

while True:
    sucesso, quadro = camera.read()
    if not sucesso:
        break

    quadro = cv2.flip(quadro, 1)
    altura, largura, _ = quadro.shape

    imagem_rgb = cv2.cvtColor(quadro, cv2.COLOR_BGR2RGB)
    resultado = maos.process(imagem_rgb)

    angulo_x = None
    angulo_y = None

    if resultado.multi_hand_landmarks and resultado.multi_handedness:
        for pontos_mao, classificacao in zip(
            resultado.multi_hand_landmarks, resultado.multi_handedness
        ):
            lado = classificacao.classification[0].label

            if lado == "Right":
                desenho.draw_landmarks(quadro, pontos_mao, mp_maos.HAND_CONNECTIONS)
                indicador = pontos_mao.landmark[8]

                angulo_x = int(indicador.x * 180)
                angulo_y = int(indicador.y * 180)

                cx = int(indicador.x * largura)
                cy = int(indicador.y * altura)
                cv2.circle(quadro, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

            elif lado == "Left":
                desenho.draw_landmarks(quadro, pontos_mao, mp_maos.HAND_CONNECTIONS)
                estado_mao_esquerda = 0 if mao_esta_fechada(pontos_mao) else 1
                texto_mao = "Fechada" if estado_mao_esquerda == 0 else "Aberta"
                cv2.putText(
                    quadro,
                    f"Mao Esquerda: {texto_mao}",
                    (50, 200),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,
                    (0, 0, 255),
                    2,
                )

    if angulo_x is not None and angulo_y is not None:
        texto = f"X: {angulo_x}  Y: {angulo_y}  Z: {estado_mao_esquerda}"
        cv2.putText(
            quadro, texto, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 2
        )
        mover_servos(angulo_x, angulo_y, estado_mao_esquerda)

    cv2.imshow("Controle com Mãos", quadro)

    if cv2.waitKey(1) & 0xFF == 27:  # Tecla ESC para sair
        break

# Encerra a comunicação
arduino.close()
camera.release()
cv2.destroyAllWindows()
