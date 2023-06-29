from typing import List


# this method parse a string for double braces, and if there are double braces found, it will return the string between the double braces
# it will work for as many double braces as there are in the string
def parseRawPromptForInputVariables(rawPrompt: str) -> List[str]:
    # check if there are double braces in the string
    if rawPrompt.count("{{") > 0 and rawPrompt.count("}}") > 0:
        # split the string by the double braces
        splitRawPrompt = rawPrompt.split("{{")

        # remove the first element of the list, since it is not needed
        splitRawPrompt.pop(0)

        # create a list to store the parsed input
        parsedInput = []

        # loop through the list of strings
        for string in splitRawPrompt:
            # split the string by the double braces
            splitString = string.split("}}")

            # add the first element of the list to the parsed input
            parsedInput.append(splitString[0])

        # return the parsed input
        return parsedInput

    # if there are no double braces in the string, return an empty list
    else:
        return []