import subprocess
from git import *
import unittest
import os


def run_bash(bash_command):
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    return process.communicate()[0]

class GitUnlock(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['PATH'] += ':' + os.path.abspath(
            os.path.join(os.path.dirname(__file__),".."))

    def setUp(self):
        self.git_path = os.environ['HOME'] + '/git-boots-test'
        os.mkdir(self.git_path)
        os.chdir(self.git_path)
        git = Git(self.git_path)
        git.init()
        with open('test.txt', 'w') as f:
            f.write('test\n')
        assert os.path.exists('test.txt')

        git.add('test.txt')
        git.commit('-m "First commit"')

        with open('.git/index.lock', 'w') as f:
            f.write('test\n')

        assert os.path.exists('.git/index.lock')

    def tearDown(self):
        run_bash('rm -rf ' + self.git_path)

    def test_git_unlock(self):
        run_bash('git-unlock')
        assert not os.path.exists('.git/index.lock')

    def test_git_unlock_exec(self):
        result = run_bash('git-unlock -e echo')
        self.assertEquals(result.strip(), '.git/index.lock')

        result = run_bash('git-unlock --exec echo')
        self.assertEquals(result.strip(), '.git/index.lock')

if __name__ == '__main__':
    unittest.main()
