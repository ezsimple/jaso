#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import unicodedata

####################################################################
## 파일명 및 폴더명을 NFC(완성형)로 변경
####################################################################
def normalize_path(path):
    # NFC로 정규화한 경로 생성
    normalized_path = unicodedata.normalize('NFC', path)

    # 경로가 변경되었는지 확인
    if path != normalized_path:
        # 수정된 경로로 변경
        os.rename(path, normalized_path)
        print(f"[+] {path} -> {normalized_path}")

####################################################################
## 변경 대상 파일 및 폴더명 찾아서 normalize_path() 호출
####################################################################
def normalize_filenames_in_directory(directory, recursive=False, target_extension=None):
    for dirpath, dirnames, filenames in os.walk(directory):
        # 현재 디렉터리에서 폴더 이름 정규화
        for dirname in dirnames:
            dir_path = os.path.join(dirpath, dirname)
            normalize_path(dir_path)

        # 파일 이름 정규화
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)

            # 특정 확장자에 해당하는 파일만 변경
            if target_extension is None or file_path.lower().endswith(target_extension.lower()):
                normalize_path(file_path)

        # 만약 recursive 옵션이 활성화되었으면, 하위 디렉터리의 탐색을 계속
        if not recursive:
            break

####################################################################
## 인자 설정 및 변경 코드 호출
####################################################################
def main():
    parser = argparse.ArgumentParser(
        description='Normalize Korean filenames and directory names in a directory.',
        usage='%(prog)s [directory] [-r|--recursive] [-e|--extension <extension>]'
    )
    parser.add_argument('directory', metavar='directory', type=str, nargs='?', default=os.getcwd(),
                        help='The target directory (default: current directory)')
    parser.add_argument('-r', '--recursive', action='store_true', help='Enable recursive search')
    parser.add_argument('-e', '--extension', type=str, default=None,
                        help='Target file extension to change (default: None)')

    args = parser.parse_args()

    target_directory = args.directory
    recursive = args.recursive
    target_extension = args.extension

    # 디렉터리 내의 특정 확장자를 가진 파일들과 폴더들의 이름을 NFC로 정규화
    normalize_filenames_in_directory(target_directory, recursive, target_extension)

if __name__ == '__main__':
    main()

