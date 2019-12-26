# [In-project modules]

# [Python native modules]
import json
# [Third-party modules]

class JSONLogger:
    def __init__(self, log_path):
        self.log_path = log_path
        self._inner_object = []
        self.load_log()
    
    def load_log(self):
        try:
            with open(self.log_path, 'r', encoding='UTF8') as fr:
                self._inner_object = json.load(fr)
                fr.close()
        except FileNotFoundError:
            self._to_file()
    def write(self, json_object):
        self._inner_object.append(json_object)
        self._to_file()
    def _to_file(self):
        with open(self.log_path, 'w', encoding='UTF8') as fw:
            json.dump(self._inner_object, fw)
            fw.flush()
            fw.close()
