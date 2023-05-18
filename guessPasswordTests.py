import datetime
import genetic
import unittest
import random


def getFitness(guess, target):
    return sum(1 for expected, actual in zip(target, guess)
               if expected == actual)


def display(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime
    print("{0}\t{1}\t{2}".format(
        candidate.Genes, candidate.Fitness, str(timeDiff)))


class GuessPasswordTests(unittest.TestCase):
    geneset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZöäüÖÄÜ0123456789!.,#*?§$£%&:;\\/`´'µ=-_<>^°@#$%{}[" \
              "]()'\"~;:.<> "

    def test_1(self):
        target = "Password123"  # easy password
        self.guess_password(target)

    def test_2(self):
        target = "23PfEFXr@AdCZY4gM=wLvbaEQ2EXZmgG"  # 32 digit password
        self.guess_password(target)

    def guessPassword(self, target):
        startTime = datetime.datetime.now()

        def fnGetFitness(genes):
            return getFitness(genes, target)

        def fnDisplay(candidate):
            display(candidate, startTime)

        optimalFitness = len(target)
        best = genetic.get_best(fnGetFitness, len(target),
                                optimalFitness, self.geneset, fnDisplay)
        self.assertEqual(best.Genes, target)

    def test_Random(self):
        length = 150
        target = ''.join(random.choice(self.geneset) for _ in
                         range(length))

        self.guess_password(target)

    def test_benchmark(self):
        genetic.Benchmark.run(lambda: self.test_Random())


if __name__ == '__main__':
    unittest.main()  # make sure the tests are ran
