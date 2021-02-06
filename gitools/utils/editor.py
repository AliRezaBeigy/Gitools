import os
import tempfile
import subprocess


class Editor:
    @staticmethod
    def input(message):
        tmp = tempfile.NamedTemporaryFile(delete=False).name
        if not message is None:
            with open(tmp, "a") as f:
                f.write(message)
        process = subprocess.Popen(
            Editor.findEditor() + [tmp], stderr=None, stdout=None
        )
        _, _ = process.communicate()

        with open(tmp) as f:
            result = f.readlines()
        os.remove(tmp)

        return "".join(result).strip()

    @staticmethod
    def findEditor():
        try:
            process = subprocess.Popen(["nano"])
            process.terminate()
            return ["nano", "-t"]
        except:
            pass

        try:
            process = subprocess.Popen(["vim"])
            process.terminate()
            return ["vim", "-n"]
        except:
            pass

        try:
            process = subprocess.Popen(["vi"])
            process.terminate()
            return ["vi", "-n"]
        except:
            pass

        try:
            process = subprocess.Popen(
                ["where", "git"],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stdin=subprocess.DEVNULL,
            )
            out, err = process.communicate()
            if not err:
                out = out.decode("utf-8")
                out = out.split("\n")[0].strip()
                out = os.path.dirname(out)
                editorPath = os.path.join(out, "..", "usr", "bin", "nano.exe")
                if os.path.exists(editorPath):
                    return [editorPath, "-t"]
                editorPath = os.path.join(out, "..", "usr", "bin", "vim.exe")
                if os.path.exists(editorPath):
                    return [editorPath, "-n"]
                editorPath = os.path.join(out, "..", "usr", "bin", "vi")
                if os.path.exists(editorPath):
                    return [editorPath, "-n"]
        except:
            pass