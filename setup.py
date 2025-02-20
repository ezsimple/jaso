from setuptools import setup  # setuptools 모듈에서 setup 함수를 가져옵니다.

APP = ['main.py']  # 애플리케이션의 진입점 파일을 지정합니다.
DATA_FILES = []  # 애플리케이션에 포함할 데이터 파일 목록입니다.
OPTIONS = {  # py2app에 전달할 옵션을 정의합니다.
    'iconfile': 'icon.icns',  # 애플리케이션 아이콘 파일 경로를 지정합니다.
    'plist': {  # 애플리케이션의 plist 설정을 정의합니다.
        'LSUIElement': True,  # 메뉴 막대 애플리케이션으로 설정합니다.
    },
    'packages': ['rumps'],  # 애플리케이션에 포함할 패키지 목록입니다.
}

setup(  # setup 함수를 호출하여 애플리케이션을 설정합니다.
    app=APP,  # 애플리케이션 목록을 지정합니다.
    name="자소",  # 애플리케이션의 이름을 지정합니다.
    description="OSX 자소분리 방지기(NFD->NFC)",  # 애플리케이션의 설명을 지정합니다.
    version="0.2.0",  # 애플리케이션의 버전을 지정합니다.
    data_files=DATA_FILES,  # 포함할 데이터 파일 목록을 지정합니다.
    options={'py2app': OPTIONS},  # py2app에 전달할 옵션을 지정합니다.
    setup_requires=['py2app'],  # 설치 시 필요한 패키지를 지정합니다.
)  # setup 함수 호출 종료
