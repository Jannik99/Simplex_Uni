import os


def readBenchmarkFiles(benchmark_dir) -> list:
    '''
    reads all Benchmark files which are .txt files in the directory ./benchmarks and returns a list of all files
    '''
    files = []
    for file in os.listdir(benchmark_dir):
        if file.endswith(".txt"):
            files.append(file)
    return files

        