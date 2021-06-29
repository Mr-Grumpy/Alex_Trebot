import os

tester = open('bipples.txt', 'a+')

tester.write("This is one line.\n")
tester.write("But this is a new line.\nSo lets see how it handles line breaks\n")


line2 = tester.read(17)
content = tester.read()
print("This is the second line: " + line2)
print("This is the whole content of the file:\n")
