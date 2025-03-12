import os  # 운영 체제와 상호작용하기 위한 os 모듈을 가져옵니다.
import unicodedata  # 유니코드 문자 정규화를 위한 unicodedata를 가져옵니다.

import rumps  # macOS 메뉴 막대 애플리케이션 생성을 위한 rumps를 가져옵니다.
from watchdog.events import FileSystemEventHandler  # 파일 시스템 이벤트를 처리하기 위한 FileSystemEventHandler를 가져옵니다.
from watchdog.observers import Observer  # 파일 시스템 변경 사항을 모니터링하기 위한 Observer를 가져옵니다.
import logging

# 운영체제의 기본 인코딩이 ASCII로 설정된 경우 sys.stdin.reconfigure()를 사용해 UTF-8을 강제로 지정할 수 있습니다.
import sys
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

logging.basicConfig(filename='jaso_debug.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def normalize_path(path: str):  # 파일 경로를 NFC 유니코드 형식으로 정규화하는 함수
    # 주어진 파일 경로의 이름을 NFC 유니코드 형식으로 정규화하고 파일명을 변경합니다.
    directory, name = os.path.split(path)  # 경로를 디렉토리와 파일 이름으로 나눕니다.
    normalized_name = unicodedata.normalize('NFC', name)  # 파일 이름을 NFC 형식으로 정규화합니다.
    if len(name) == len(normalized_name):  # 이름이 이미 정규화되어 있는지 확인합니다.
        return  # 정규화된 경우 아무것도 하지 않습니다.

    normalized_path = os.path.join(directory, normalized_name)  # 새로운 정규화된 경로를 생성합니다.
    os.rename(path, normalized_path)  # 파일을 정규화된 경로로 이름을 변경합니다.


def normalize_filenames_in_directory(directory):  # 디렉토리 내 파일 이름을 정규화하는 함수
    # 주어진 디렉토리와 그 하위 폴더에 있는 모든 파일의 이름을 NFC로 정규화합니다.
    for dir_path, child_dir_names, filenames in os.walk(directory):  # 디렉토리를 탐색합니다.
        for filename in filenames:  # 각 파일 이름을 반복합니다.
            file_path = os.path.join(dir_path, filename)  # 전체 파일 경로를 가져옵니다.
            normalize_path(str(file_path))  # 파일 경로를 정규화합니다.
        for dir_name in child_dir_names:  # 하위 디렉토리를 반복합니다.
            child_dir_path = os.path.join(dir_path, dir_name)  # 전체 디렉토리 경로를 가져옵니다.
            normalize_path(str(child_dir_path))  # 디렉토리 경로를 정규화합니다.
        break  # 첫 번째 레벨의 디렉토리 탐색 후 종료합니다.

class Watcher:  # 파일 시스템 변경을 감시하는 클래스
    def __init__(self, directories_to_watch):  # Watcher 클래스의 생성자
        self.directories_to_watch = directories_to_watch  # 감시할 디렉토리 목록을 설정합니다.
        self.observer = Observer()  # 새로운 옵저버 인스턴스를 생성합니다.

    def run(self):  # 옵저버를 시작하는 메서드
        event_handler = Handler()  # 이벤트 핸들러 인스턴스를 생성합니다.

        for directory in self.directories_to_watch:  # 각 디렉토리에 대해
            self.observer.schedule(event_handler, directory, recursive=True)  # 이벤트 핸들러를 예약합니다.

        self.observer.start()  # 옵저버를 시작합니다.

        def _maintainer(timer: rumps.Timer):  # 옵저버 상태를 유지하는 내부 메서드
            if self.observer.is_alive():  # 옵저버가 여전히 실행 중인지 확인합니다.
                self.observer.join(1)  # 옵저버가 종료될 때까지 대기합니다.

        self.timer = rumps.Timer(_maintainer, 1)  # 타이머를 설정합니다.
        self.timer.start()  # 타이머를 시작합니다.

    def stop(self):  # 옵저버를 중지하는 메서드
        try:
            self.observer.stop()  # 옵저버를 중지합니다.
            self.observer.join()  # 옵저버가 종료될 때까지 대기합니다.
        except:
            pass
        finally:
            self.timer and self.timer.stop()  # 타이머를 중지합니다.

class Handler(FileSystemEventHandler):  # 파일 시스템 이벤트 핸들러 클래스
    # 파일 시스템 이벤트에 반응하여 적절한 조치를 취하는 이벤트 핸들러 클래스입니다.
    @staticmethod
    def on_any_event(event):  # 모든 파일 시스템 이벤트에 반응하는 메서드
        if event.event_type == 'created':  # 파일이 생성된 경우
            normalize_filenames_in_directory(event.src_path)  # 파일 이름을 정규화합니다.
        elif event.event_type == 'modified':  # 파일이 수정된 경우
            normalize_filenames_in_directory(event.src_path)  # 파일 이름을 정규화합니다.
        elif event.event_type == 'moved':  # 파일이 이동된 경우
            normalize_filenames_in_directory(event.dest_path)  # 파일 이름을 정규화합니다.


class JasoRumpsApp(rumps.App):  # macOS 메뉴 막대 애플리케이션 클래스
    # macOS 메뉴바 앱을 위한 클래스입니다.

    def __init__(self, *args, **kwargs):  # JasoRumpsApp 클래스의 생성자
        icon_path = "icon.icns"  # 애플리케이션 아이콘 경로
        super().__init__(name="자소", icon=icon_path, quit_button=None)  # 애플리케이션을 초기화합니다.

        self.watcher: Watcher | None = None  # 감시기를 초기화합니다.
        self.icon_path = icon_path  # 아이콘 경로를 저장합니다.

    @rumps.clicked("자동변환 시작")  # "자동변환 시작" 버튼 클릭 이벤트 처리
    def _start(self, _):  # 자동변환 시작 버튼 클릭 이벤트 처리 메서드
        try:
            if self.watcher:  # 감시기가 이미 실행 중인 경우
                self.watcher.stop()  # 감시기를 중지합니다.
                rumps.alert(message="이미 실행 중이던 작업을 중단했습니다.", icon_path=self.icon_path)  # 경고 메시지를 표시합니다.
            window = rumps.Window(title="자소", message="한글 자소분리를 방지할 폴더 주소를 입력해주세요.", dimensions=(200, 20))  # 입력 창을 표시합니다.
            window.icon = self.icon_path  # 아이콘을 설정합니다.
            response = window.run()  # 입력 창을 실행합니다.

            # 사용자 home 디렉토리 가져오기
            home_path = os.path.expanduser("~")

            # Construct paths to Documents, Downloads, and Desktop
            documents_path = os.path.join(home_path, "Documents")
            downloads_path = os.path.join(home_path, "Downloads")
            desktop_path = os.path.join(home_path, "Desktop")

            # 기본 경로 목록 생성
            paths_to_watch = [documents_path, downloads_path, desktop_path]  # 기본 경로 목록

            # ~/.env 를 통한 경로 추가
            try:
                with open(os.path.join(home_path, ".env"), encoding='utf-8') as f:
                    paths_to_watch.extend(next((line.split('=')[1].strip().split(',') for line in f if line.startswith("JASO_DIRS=")), []))
            except FileNotFoundError:
                pass

            # 앱 입력창을 통한 경로 추가
            if response.clicked:  # 입력 창에서 확인 버튼을 클릭한 경우
                directory_path = response.text  # 입력된 폴더 경로를 가져옵니다.

                if directory_path and os.path.isdir(directory_path):  # 입력된 경로가 유효한 디렉토리인 경우
                    paths_to_watch.append(directory_path)  # 유효한 경로를 목록에 추가합니다

                # 경고 메시지를 표시합니다.
                rumps.alert("이제부터 지정 폴더에서는 자동으로 한글의 자소분리가 방지됩니다.", icon_path=self.icon_path)  # 성공 메시지를 표시합니다.
                rumps.alert(f"감시폴더: {', '.join(paths_to_watch)}", icon_path=self.icon_path)
                self.watcher = Watcher(paths_to_watch)  # 감시기를 초기화합니다.
                self.watcher.run()  # 감시기를 시작합니다.
        
            print(paths_to_watch)

        except Exception as e:  # 예외가 발생한 경우
            rumps.alert(f"오류: {str(e)}")  # 오류 메시지를 표시합니다.

    @rumps.clicked("종료")  # "종료" 버튼 클릭 이벤트 처리
    def _quit(self, _):  # 종료 버튼 클릭 이벤트 처리 메서드
        self.watcher and self.watcher.stop()  # 감시기를 중지합니다.
        rumps.quit_application()  # 애플리케이션을 종료합니다.


if __name__ == "__main__":  # 스크립트가 직접 실행되는지 확인합니다.
    app = JasoRumpsApp()  # JasoRumpsApp의 인스턴스를 생성합니다.
    app.run()  # 애플리케이션을 실행합니다.
