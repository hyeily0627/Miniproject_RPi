# Miniproject_RPi
미니프로젝트 라즈베리파이

# LED CONTROLER
- 기간 : 2024-06-28
- 설명 : LED 컨트롤러에 원하는 색상(빨,청,녹,흰)을 누르면 출력되는 기능
- 작동영상 

https://github.com/hyeily0627/Miniproject_RPi/assets/156732476/7a36c6ac-295f-409b-add9-6d51dd3ba130


# LED CONTROLER ++ 
- 기간 : 2024-06-29 ~ 2024-07-02
- 설명 : LED 컨트롤러 + 온습도 센서 및 부저를 부착하여 스마트홈 기능을 구현
- 라즈베리파이 연결

![연결](https://raw.githubusercontent.com/hyeily0627/Miniproject_RPi/main/images/001.jpg)

- 작동영상

https://github.com/hyeily0627/Miniproject_RPi/assets/156732476/2fcc6b23-07c3-4e8e-8bbb-3fa32a6c7db7

- 온습도 및 부저 컨트롤 코드
    ```python
    def update_list_view(self, data):
        self.model.setStringList(data)
        if len(data) > 1 and "Humidity" in data[1]:
            humidity = float(data[1].split(':')[1].strip('%'))
            if humidity < 50: # 부저가 울릴 습도값 지정 
                Buzz.stop()
            else:
                Buzz.start(50)
    ```

- UI 변경(최종)
![ui](https://raw.githubusercontent.com/hyeily0627/Miniproject_RPi/main/images/001.png)

## 추가적 개발 사항
- 습도별 LED 컨트롤을 할 수 있는 기능
    - 습도 80% 이상이면 Red Led On , 습도 20~80% Blue Led On과 같은 범위 값 
