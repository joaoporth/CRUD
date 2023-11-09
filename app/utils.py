import re


def clean(text) -> str:
	return str(re.sub(r'[^\w\s]', '', str(text))).replace(' ','').strip()


