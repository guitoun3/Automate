def parse(s, alphabet):
	print "parsing string "+s
	l = []
	index = 0
	operands="+*."
	left = ""
	right = ""
	operand = ""
	if s[index] in alphabet:
		left = s[index]
	elif s[index] in operands:
		return ["MISFORMATED STRING"]
	elif s[index] == '(':
		index+=1
		while s[index] != ')':
			if index == len(s)-2:
				return ["MISFORMATED STRING"]
			else:
				left+=s[index];
				index+=1
		if left == "":
			return ["MISFORMATED STRING"]
		index+=1
		if s[index] not in operands:
			return ["MISFORMATED STRING"]
		else:
			operand = s[index]
		return [operand, parse(left, alphabet)]
	index+=1
	right = ""
	if s[index] in operands:
		operand = s[index]
		while index < len(s):
			right+=s[index]
			index+=1
		return [operand, left, parse(right, alphabet)]
	else:
		while index < len(s):
			right+=s[index]
			index+=1
		return [".", left, parse(right, alphabet)]

	return l

print parse(raw_input(), "abcdef")