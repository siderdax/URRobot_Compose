# UR_ROS2

ROS2 Humble + Universal Robot + Mosquitto

ROS2를 통한 유니버설 로봇 제어 환경 구축

## 준비

1. 사용하려는 운영체제 선택
   1. 가능한 운영체제
      1. Ubuntu 22.04
      2. Windows 10 (+WSL)
      
      

## 설치 및 실행

### Ubuntu 22.04

1. Docker engine 설치

   1. [설치 매뉴얼](https://docs.docker.com/engine/install/ubuntu/#installation-methods)
   2. 선택사항
      1. [sudo 없이 docker 사용](https://docs.docker.com/engine/install/linux-postinstall/)

2. ```bash
   git clone http://wtcontrol:7990/scm/bcs/ur_ros2.git
   cd ur_ros2
   # 실행
   docker compose up
   ```

3. ```bash
   # 종료
   docker compose down
   ```

   

### Windows 10

#### Docker Desktop을 통해 사용하는 방법

1. Windows 운영체제 환경에서는 Docker Engine을 사용할 수 없어 Docker Desktop을 설치해야 함

   - Apache 2.0 License인 Docker Engine과 다르게 Docker Desktop의 경우 상업용으로 사용할 경우 라이센스 문제가 있음
   - https://docs.docker.com/subscription/desktop-license/
   - [설치 매뉴얼](https://docs.docker.com/desktop/install/windows-install/)

2. Powershell을 실행 후 아래 명령 실행

3. ```powershell
   # 실행
   docker compose up
   ```

4. ```powershell
   # 종료
   docker compose down
   ```

   

#### Ubuntu 22.04 WSL + Docker Engine을 설치해 사용하는 방법

1. Windows Store에서 Ubuntu 22.04 설치
2. Docker engine 설치
   - Ubuntu 22.04에서 Docker 설치 방법(APT 또는 설치 쉘 스크립트 사용)과 동일
3. ```bash
   git clone http://wtcontrol:7990/scm/bcs/ur_ros2.git
   cd ur_ros2
   # 실행
   docker compose up
   ```

4. ```bash
   # 종료
   docker compose down
   ```

## 

## 트러블슈팅

1. "docker compose up"에서 컨테이너 빌드 중 에러 발생 시
   1. docker compose down 후 재시도로 해결 가능



## 테스트

1. MQTTSample 앱 빌드 후 실행
   1. http://wtcontrol:7990/projects/BCS/repos/mqttsample/browse
2. 로컬 환경이라면 127.0.0.1:1884에 접속 후 urscript토픽으로 ur스크립트 publish
   1. 원격 환경이라면 127.0.0.1이 아닌 해당 PC IP주소로 연결



## 커스터마이징

1. MQTT 포트 변경

   1. MQTT Broker가 이미 설치된 환경에서는 MQTT에서 사용하는 기본 값 포트 1883이 이미 사용 중일 수 있어 1884포트를 사용하도록 compose.yaml에 지정되어 있음. 아래와 같이 변경 가능

   2. ```yaml
      #compose.yaml
      ...
      mosquitto:
          image: eclipse-mosquitto
          restart: always
          ports:
      #      - 1884:1883
             - 1884:1884
          volumes:
            - ./mosquitto/mosquitto.conf:/mosquitto/config/mosquitto.conf
          networks:
            ur_net:
              ipv4_address: 192.168.56.2
      ...
      ```

2. MQTT Topic 변경

   1. 기본 값은 "urscript"지만 원하는 토픽으로 변경 가능

   2. ```yaml
      #compose.yaml
       ros_mqtt:
         build:
           context: ros_mqtt
           dockerfile: Dockerfile
         environment:
            - MQTT_HOST=192.168.56.2
            - MQTT_PORT=1883
      #      - MQTT_TOPIC=urscript
            - MQTT_TOPIC=custom_topic_name
            - MQTT_ROLE=subscriber
            - NODE_NAME=urscript_mqtt_sub
            - ROS_TOPIC_NAME=/urscript_interface/script_command
         networks:
            ur_net:
              ipv4_address: 192.168.56.102
         depends_on:
            - mosquitto
      ```

      

