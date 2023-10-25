import os
import shutil
import subprocess
from glob import glob
from typing import List

from tqdm import tqdm

from testcase_generator import InputGenerator


class GeneratorSystem:
    INPUT_DIR = "input"
    OUTPUT_DIR = "output"

    def __prepareIOFolders(self) -> None:
        if not os.path.exists(GeneratorSystem.INPUT_DIR):
            os.makedirs(GeneratorSystem.INPUT_DIR)
        if not os.path.exists(GeneratorSystem.OUTPUT_DIR):
            os.makedirs(GeneratorSystem.OUTPUT_DIR)

        for file in glob(f"{GeneratorSystem.INPUT_DIR}/*"):
            os.remove(file)
        for file in glob(f"{GeneratorSystem.OUTPUT_DIR}/*"):
            os.remove(file)

    def __generateInputFiles(self) -> None:
        inputs = InputGenerator().generate()
        print("Generating input files...")
        for inputIndex, input in enumerate(tqdm(inputs)):
            with open(os.path.join(self.INPUT_DIR, f"input_{inputIndex}.txt"), "w") as inputFile:
                inputFile.write(f"{input.n}\n")
                inputFile.write(" ".join(map(str, input.a)))

    def __generateOutputFiles(self) -> None:
        print("Generating output files...")
        self.__compileSolver()
        for inputFile in tqdm(glob(f"{GeneratorSystem.INPUT_DIR}/*")):
            self.__runSolver(inputFile)

    def __zipTestCases(self) -> None:
        print("Zipping the test cases into `testcases.zip`...")
        shutil.copytree("input", "testcases/input")
        shutil.copytree("output", "testcases/output")
        shutil.make_archive("testcases", "zip", "testcases")
        shutil.rmtree("testcases")

    def __compileSolver(self) -> None:
        subprocess.run(["g++", "sol.cpp", "-O2"])

    def __runSolver(self, inputFilePath: str):
        caseNo = inputFilePath.split(".")[0].split("_")[-1]
        # ./a.out for Linux!
        subprocess.run(["./a.exe", inputFilePath, os.path.join(self.OUTPUT_DIR, f"output_{caseNo}.txt")])

    def run(self) -> None:
        self.__prepareIOFolders()
        self.__generateInputFiles()
        self.__generateOutputFiles()
        self.__zipTestCases()


if __name__ == "__main__":
    GeneratorSystem().run()
