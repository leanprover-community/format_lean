import os, subprocess, json

class LeanError(Exception):
    pass

class Server:
    """
    Very rough interface around the Lean server. Will work only if nothing bad
    happens/
    """
    def __init__(self, lean_exec_path, lean_path):
        self.proc = subprocess.Popen([lean_exec_path, "-j0", "--server"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            universal_newlines=True, bufsize=1,
            env={'LEAN_PATH': lean_path})
        self.seq_num = 0

    def sync(self, filename):
        self.seq_num += 1
        s = f'{{"seq_num": {self.seq_num}, "command": "sync", "file_name": "{filename}"}}\n'
        self.proc.stdin.write(s)
        self.proc.stdout.readline()

    def info(self, filename, line, col):
        self.seq_num += 1
        s = f'{{"seq_num": {self.seq_num}, "command":"info", ' \
            f'"file_name": "{filename}", ' \
            f'"line": {line},"column":{col}}}\n'
        self.proc.stdin.write(s)
        ret = json.loads(self.proc.stdout.readline().rstrip())
        try:
            return ret['record']['state']
        except KeyError:
            raise LeanError(str(ret))
