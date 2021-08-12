"""Running CNS scripts"""
import subprocess
from haddock.error import CNSRunningError, JobRunningError
from haddock.parallel import Scheduler
import shlex
from haddock.defaults import CNS_EXE, NUM_CORES


class Job:
    """A job to be executed by the engine"""
    def __init__(self, input, output, executable, *args):
        self.input = input
        self.output = output
        self.executable = executable
        self.args = args

    def run(self):
        cmd = ''
        if self.args:
            cmd = f"{self.executable} {' '.join(map(str, self.args))}"
            self.executable = shlex.split(cmd)

        # capture output to stdout
        cmd += f' {self.input}'
        with open(self.output, 'w') as outf:
            p = subprocess.Popen(shlex.split(cmd), 
                                 stdout=outf,
                                 close_fds=True)
            out, error = p.communicate()
        p.kill()

        if error:
            raise JobRunningError(error)
        return out


class CNSJob:
    """A CNS job script"""
    def __init__(self, input_file, output_file, cns_folder='.',
                 cns_exec=CNS_EXE):
        """
        :param input_file: input CNS script
        :param output_file: CNS output
        :cns_folder: absolute execution path
        :cns_exec: CNS binary including absolute path
        """
        self.input_file = input_file
        self.output_file = output_file
        self.cns_folder = cns_folder
        self.cns_exec = cns_exec

    def run(self):
        """Run this CNS job script"""
        with open(self.input_file) as inp:
            with open(self.output_file, 'w+') as outf:
                env = {'RUN': self.cns_folder}
                p = subprocess.Popen(self.cns_exec,
                                     stdin=inp,
                                     stdout=outf,
                                     close_fds=True,
                                     env=env)
                out, error = p.communicate()
                p.kill()
                if error:
                    raise CNSRunningError(error)
        return out


class Engine:
    """Execution engine"""
    def __init__(self, jobs, num_cores=0):
        self.jobs = jobs
        if num_cores:
            self.num_cores = num_cores
        elif (num_jobs := len(jobs)) > 1:
            self.num_cores = min(num_jobs, NUM_CORES)
        else:
            self.num_cores = 1

    def run(self):
        """Run all provided jobs"""
        scheduler = Scheduler(self.jobs, self.num_cores)
        scheduler.execute()
