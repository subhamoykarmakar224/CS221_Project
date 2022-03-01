import multiprocessing
import os


class ConstructL2Index:
    def __init__(self, logging):
        self.logging = logging
        self.ioi_folder_path = os.path.join('.', 'Indexer', 'ioi')

    def create_ioi_folder(self):
        if not os.path.isdir(self.ioi_folder_path):
            os.mkdir(self.ioi_folder_path)

    def get_icluster_folder(self):
        return os.listdir(
            os.path.join('.', 'Indexer', 'iclusters')
        )

    def get_list_of_files(self, path):
        l = []
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".txt"):
                    l.append(os.path.join(root, file))
        return l

    def _worker(self, path):
        files = self.get_list_of_files(path)
        for f_path in files:
            lines = []
            with open(f_path, 'r') as f:
                lines = f. readlines()

            for i in range(len(lines)):
                try:
                    tmp = lines[i].split('||')
                    if len(tmp) >= 4:
                        tmp[2] = int(tmp[2])
                        lines[i] = tmp
                    else:
                        lines[i] = ['', '', 0, '', '']
                except:
                    self.logging.error(f'Error parsing: {tmp}')
                    lines[i] = ['', '', 0, '', '']
            
            lines = sorted(lines, key=lambda x: x[2], reverse=True)

            with open(f_path, 'w') as f:
                for l in lines:
                    if l[2] != 0:
                        l[2] = str(l[2])
                        f.write('||'.join(l))

    def controller(self):
        self.create_ioi_folder()
        clusters = [os.path.join('.', 'Indexer', 'iclusters', folder)
                    for folder in self.get_icluster_folder()]
        for c in clusters:
            self.logging.info(f'Parsing cluster: {c}')
            self._worker(c)
