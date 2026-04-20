# uciapp_manager.py
# -*- coding: utf-8 -*-

import sys
import os
import subprocess

class UCIReader(object):
    # True | False
    IS_WIN = False
    def __init__(self, uci_dir=None):
        """
        :param uci_dir: UCI 파일이 있는 디렉토리
        """
        self.uci_dir = uci_dir
        self.usewin_config = sys.platform.startswith('win')
        UCIReader.IS_WIN = self.usewin_config

    # ---------------- Windows용 파일 파서 ----------------
    def _parse_file(self, config_file):
        config = {}
        sections_order = []
        current_section = None

        if not os.path.isfile(config_file):
            return config, sections_order

        with open(config_file, 'r') as f:
            for line in f:
                raw_line = line.rstrip('\n')
                line = raw_line.strip()

                if not line or line.startswith('#'):
                    sections_order.append((None, raw_line))
                    continue

                if line.startswith('config '):
                    parts = line.split()

                    section_type = parts[1]

                    # section name이 없는 경우 처리
                    if len(parts) > 2:
                        section_name = parts[2].strip("'")
                    else:
                        # 이름 없으면 type을 이름으로 사용
                        section_name = section_type

                    current_section = section_name
                    config[current_section] = {}

                    sections_order.append((current_section, raw_line))

                elif line.startswith('option ') and current_section:
                    _, key, value = line.split(' ', 2)
                    value = value.strip("'")

                    # 타입 자동 변환
                    if value.isdigit():
                        value = int(value)
                    else:
                        try:
                            value = float(value)
                        except ValueError:
                            pass

                    config[current_section][key] = value

                    sections_order.append((current_section, raw_line))

                else:
                    sections_order.append((None, raw_line))
        return config, sections_order

    # ---------------- Windows용 파일 저장 ----------------
    def _write_file(self, config_file, config_dict, sections_order):
        lines = []

        for sec, line in sections_order:

            if sec is None:
                lines.append(line)
                continue

            if line.strip().startswith('config '):
                lines.append(line)

            elif line.strip().startswith('option '):
                parts = line.strip().split(' ', 2)
                key = parts[1]

                value = config_dict.get(sec, {}).get(key)

                if value is None:
                    value = parts[2].strip("'")

                lines.append("    option {} '{}'".format(key, value))

        with open(config_file, 'w') as f:
            f.write('\n'.join(lines) + '\n')

    # ---------------- 읽기 ----------------
    def get(self, config, section, option):
        if self.usewin_config:
            if not self.uci_dir:
                raise ValueError("Windows 테스트용으로 uci_dir 필요")

            file_path = os.path.join(self.uci_dir, config)
            uci_dict, _ = self._parse_file(file_path)

            return uci_dict.get(section, {}).get(option)

        else:
            cmd = ['uci']
            if self.uci_dir:
                cmd.extend(['-c', self.uci_dir])
            cmd.extend(['get', '{}.{}.{}'.format(config, section, option)])

            try:
                result = subprocess.check_output(cmd)
                return result.decode().strip()
            except subprocess.CalledProcessError:
                return None

    # ---------------- 쓰기 ----------------
    def set(self, config, section, option, value):
        if self.usewin_config:
            if not self.uci_dir:
                raise ValueError("Windows 테스트용으로 uci_dir 필요")
            file_path = os.path.join(self.uci_dir, config)
            uci_dict, sections_order = self._parse_file(file_path)

            sec_key = section
            if sec_key not in uci_dict:
                uci_dict[sec_key] = {}
                sections_order.append((sec_key, "config {} '{}'".format(config, section)))

            uci_dict[sec_key][option] = str(value)
            self._write_file(file_path, uci_dict, sections_order)
            return True
        else:
            # OpenWrt uci set + commit
            cmd_set = ['uci']
            if self.uci_dir:
                cmd_set.extend(['-c', self.uci_dir])
            cmd_set.extend(['set', '{}.{}.{}={}'.format(config, section, option, value)])
            try:
                subprocess.check_call(cmd_set)
                # commit
                cmd_commit = ['uci']
                if self.uci_dir:
                    cmd_commit.extend(['-c', self.uci_dir])
                cmd_commit.extend(['commit', config])
                subprocess.check_call(cmd_commit)
                return True
            except subprocess.CalledProcessError:
                return False
                
    @staticmethod
    def show_and_filter(keyword):
        if UCIReader.IS_WIN == False:
            cmd = ['uci']
            cmd.append('show')

            try:
                result = subprocess.check_output(cmd).decode('utf-8', 'replace')
                lines = result.splitlines()
                return [line for line in lines if keyword in line]
            except subprocess.CalledProcessError:
                return []
        else:
            return []

                
# ---------------- 사용 예제 ----------------
if __name__ == "__main__":
    # Windows 테스트용
    uci = UCIReader(uci_dir='./test_uci')
    print("Before set:", uci.get('test_config', 'lan', 'ipaddr'))
    uci.set('test_config', 'lan', 'ipaddr', '192.168.100.1')
    print("After set:", uci.get('test_config', 'lan', 'ipaddr'))

    # OpenWrt 예시
    # uci = UCIReader(uci_dir='/nct11af')
    # print(uci.get('network', 'lan', 'ipaddr'))
    # uci.set('network', 'lan', 'ipaddr', '192.168.1.200')
