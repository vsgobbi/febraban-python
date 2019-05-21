from collections import namedtuple
from .libs.middlewares.row import validateFormatter
from .characterType import numeric, alphaNumeric

RowStruct = namedtuple("RowStruct", ("start", "end", "len", "type", "value"))

defaultCharacters = {
    numeric:      "0",
    alphaNumeric: " ",
}


def emptyStruct(start, end, characterType):
    return RowStruct(start, end, end - start, characterType, "")


class Row:

    @classmethod
    def setStructs(cls, structs, content):
        for struct in structs:
            if isinstance(struct, tuple) and not isinstance(struct, RowStruct):
                struct = RowStruct(*struct)

            replacement = cls._formatted(
                string=str(struct.value),
                charactersType=struct.type,
                numberOfCharacters=struct.len,
                defaultCharacter=defaultCharacters[struct.type]
            )
            content = content[:struct.start] + replacement + content[struct.start + struct.len:]
        return content

    @classmethod
    @validateFormatter
    def _formatted(cls, string, charactersType, numberOfCharacters, defaultCharacter=" "):
        """
            This method fix the received String and a default complement according the alignment
            and cut the string if it' bigger than number of characters

            Args:
                string:             String to be completed
                charactersType:     Can be .numeric or .alphaNumeric
                numberOfCharacters: Integer that represents the max string len
                defaultCharacter:   Single string with default character to be completed if string is short
            Returns:
                String formatted
        """
        if not isinstance(string, str):      return defaultCharacter * numberOfCharacters
        if len(string) > numberOfCharacters: return string[:numberOfCharacters]
        if charactersType == numeric:        return defaultCharacter * (numberOfCharacters - len(string)) + string
        if charactersType == alphaNumeric:   return string + defaultCharacter * (numberOfCharacters - len(string))
        return string
