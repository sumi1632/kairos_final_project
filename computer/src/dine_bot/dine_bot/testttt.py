from pymycobot.mycobot import MyCobot
import time
# MyCobot 초기화
mycobot = MyCobot('/tty/USB0', 115200)
mycobot.set_gripper_mode(0)
mycobot.init_eletric_gripper()
mycobot.set_gripper_state(0, 50)
def fan_handling():
    """조리 완료된 음식 담기"""
    try:
        mycobot.set_gripper_mode(0)
        mycobot.init_eletric_gripper()
        mycobot.set_gripper_state(0, 50)
        print("팬 다시 잡기 웨이 포인트1")
        mycobot.send_angles([-5.18, -6.32, 10.45, 2.1, -87.53, 6.5], 30)
        time.sleep(5)
        print("팬 다시 잡기 웨이 포인트2")
        mycobot.send_angles([-2.54, -15.9, 19.59, 5.62, 93.6, 6.15], 30)
        time.sleep(5)
        print("팬 잡기 위치")
        mycobot.send_angles([3.77, -51.41, -1.05, -38.58, 91.23, 1.23], 30)
        time.sleep(5)
        print("그리퍼 닫기")
        mycobot.set_gripper_state(1, 100)  # 그리퍼 닫기
        time.sleep(4)
        print("팬 들어 올림")
        mycobot.send_angles([-4.21, -2.98, -5.18, -33.13, 95.18, -3.25], 30)
        time.sleep(5)
        print("팬 들어 올림2 ")
        mycobot.send_angles([140.21, -2.98, -5.18, -33.13, 95.18, -3.25], 30)
        time.sleep(5)
        # print("AGV 위 접시로 접근")
        # mycobot.send_angles([144.66, -29.88, -1.4, -11.51, 65.03, -16.17], 30)
        # time.sleep(5)
        print("쏟기 - 블로키로 예정")
        # 쏟기 동작 블로키 명령 추가 예정
        mycobot.send_angles([144.75, -45.43, 37.0, -20.3, 58.71, -37.17], 30)
        time.sleep(5)
        mycobot.send_angles([158.55, -66.5, 13.79, -27.68, -31.64, -33.66], 30)
        time.sleep(5)
        mycobot.send_angles([158.9, -4.21, 25.4, -26.19, 17.13, -13.27], 30)
        time.sleep(5)
        # print("쏟고 들어 올리기")
        # mycobot.send_angles([130.16, -2.98, -2.54, -49.21, 92.1, -19.86], 30)
        # time.sleep(5)
        print("팬 원위치 웨이 포인트")
        mycobot.send_angles([1.75, 1.23, 1.23, -44.2, 86.57, -17.22], 30)
        time.sleep(5)
        print("팬 내려놓기 위치")
        mycobot.send_angles([3.77, -51.41, -1.05, -38.58, 91.23, 1.23], 30)
        time.sleep(5)
        print("그리퍼 열기")
        mycobot.set_gripper_state(0, 100)  # 그리퍼 열기
        time.sleep(4)
        print("조리 완료된 음식 담기 동작 완료")
    except Exception as e:
        print(f"fan_handling 중 오류 발생: {e}")
        raise e
# 메인 함수 실행
if __name__ == "__main__":
    fan_handling()