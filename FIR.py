"""
Module: FIR
Project: FIR
Description: 

Date: 10/14/2018
Author: John J. Hritz
Email: john-j-hritz@sbcglobal.net
"""


class FIR:
    # Implements a Finite Impulse Response Filter

    # Constructor
    def __init__(self, coefs):
        self.length = len(coefs)  # the number of IR coefficients in the filter
        self.impulseResponse = coefs  # stores the IR coefficients
        self.delayLine = [0.0] * self.length  # keeps track of the most recent inputs
        self.count = 0  # tracks where the next input should go on the delay line.
        #   Removes the need for shifting on each iteration.

    # end __init__

    # Takes a list of input samples and returns the output based on the FIR's response coefficients
    def getOutputSample(self, inputSample):
        index = self.count  # update the index so we know where we're putting this new sample
        self.delayLine[index] = inputSample  # add the sample to the delay line
        result = 0.0  # reset the result so we start fresh

        for coef in self.impulseResponse:  # multiply every sample on the delay line by every coefficient
            result += coef * self.delayLine[
                index]  # multiply the coefficient by the sample and add it to the running tally
            index -= 1  # decrement the index

            if index < 0:  # if the index goes negative, reset it to the end of the delay line
                index = self.length - 1
            # end if
        # end for

        self.count += 1  # increment the count, so we know where the next sample goes
        if self.count >= self.length:  # if the count goes out of bounds, reset it to the beginning of the
            self.count = 0  # delay line
        # end if

        return result
    # end getOutputSample


def main():
    import math  # needed for the log function
    import matplotlib.pyplot as plt  # 3rd party library: https://matplotlib.org/users/installing.html

    FIRCoefs = [-9, 0, 73, 128, 73, 0, -9]  # the response coefficients of the FIR

    testFIR = FIR(FIRCoefs)  # the FIR to be tested

    output = list()  # list to store the outputs of the function

    for sigInput in range(-1400, 1400):  # test each signal in the range
        output.append(testFIR.getOutputSample(sigInput))
    # end for

    # the bit size will be determined by the largest absolute value in the output
    outputMax = max(output)
    outputMin = min(output)
    print(str(outputMax) + ", " + str(outputMin))

    # find the largest absolute value in the list
    absMax = max(abs(outputMax), abs(outputMin))

    # take the 2nd log of the absolute maximum to find the number of bits required
    absMaxLog = math.log(absMax, 2)
    print(absMaxLog)

    # Can't have a partial bit, so we need to round up
    print(math.ceil(absMaxLog))

    plt.plot(output)
    plt.show()


# end main

if __name__ == "__main__":
    main()
