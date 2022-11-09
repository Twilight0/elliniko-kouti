import unicodedata
import re
import os


def strip_accents(text):

    result = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

    return result



def sanitize(text, dont_change_case=False, level=2):

    if level >= 2:
        text = strip_accents(text)

    if not dont_change_case and level >= 1:
        text = re.sub(r',?\s([Α-Ω])', lambda txt: txt.group().lower(), text)
        text = re.sub(r'[.!;?]\s(\D)', lambda txt: txt.group().upper(), text)

    if level >= 2:
        text = text.replace(';', '?')

    if level >= 1:
        text = text.replace(u'π.χ.', u'πχ')

        filename = os.path.join(os.path.dirname(__file__), 'names.txt')

        with open(filename, 'r', encoding='utf-8') as f:
            names = f.read().splitlines()

        if not dont_change_case and level >= 1:
            text = ' '.join(
                w.capitalize() if any([w.capitalize().strip('!.;?,') == n for n in names]) else w for w in text.split()
            )

        text = fix_time(text)

    return text


def greeklish2greek(text):

    text = text.lower()

    text = re.sub("th|[kp]s|\w", lambda c: chr(1023 & "abgdezh8iklmn3opr_styfx4w".find(c[0]) % (824 + 2 * ord(c[0][0])) - 79), text)

    text = re.sub(r'σ( )|σ$', r'ς\1', text)

    text = text.replace('ϐ', 'θ').replace('ϒ', 'υ')

    return text


def fix_parenthesis(text):

    text = re.sub(r'(\w)\( ?', r'\1 (', text)
    text = re.sub(r' \)(\w)', r') \1', text)
    text = text.replace(' )', ')')
    text = text.replace('( ', '(')

    return text

def fix_commas(text):

    text = re.sub(r',(\S)', r', \1', text)
    text = re.sub(r' ,(\S)', r', \1', text)
    text = text.replace(' , ', ', ')

    return text
    
def fix_abbreviations(text):
	
	text = text.replace(u'ΧΑΡ/ΡΑΣ', u'ΧΑΡΑΚΤΗΡΑΣ')
	text = text.replace(u'ΧΑΡΡΑΣ', u'ΧΑΡΑΚΤΗΡΑΣ')
	
	return text


def fix_slashes(text):

    text = re.sub(r' ?(/{2,}) ?', r' // ', text)
    text = text.replace('\\', '/')

    return text


def fix_spaces(text):

    text = re.sub(r' {4,}', r'\n', text)
    text = re.sub(r'  ? ?', r' ', text)

    return text


def fix_dashes(text):

    text = re.sub(r' ?-{2,} ?', r' -- ', text)

    return text

def fix_time(text):

    text = text

    return text


def latin2greek(text, replace='yes'):

    words = [
        (u'Okay', u'Οκ'), (u'OKAY', u'ΟΚ'), (u'okay', u'οκ'), (u'Site', u'Σαιτ'),
        (u'site', u'σαιτ'), (u'SITE', u'ΣΑΙΤ'), (u'Sex', u'Σεξ'), (u'SEX', u'ΣΕΞ'),
        (u'Sexting', u'Σεξτινγκ'), (u'sexting', u'σεξτινγκ'), (u'SEXTING', u'ΣΕΞΤΙΝΓΚ'),
        (u'Service', u'Σερβις'), (u'service', u'σερβις'), (u'SERVICE', u'ΣΕΡΒΙΣ'),
        (u'Social', u'Σοσιαλ'), (u'social', u'σοσιαλ'), (u'SOCIAL', u'ΣΟΣΙΑΛ'),
        (u'Netflix', u'Νετφλιξ'), (u'netflix', u'νετφλιξ')
    ]

    if replace == 'yes':

        for w in words:

            text = text.replace(w[0], w[1])
            if w[1] == text:
                break

        return text

    elif replace == 'reverse':

        for w in words:

            text = text.replace(w[1], w[0])
            if w[0] == text:
                break

        return text

    elif replace == 'no':

        return text

    else:

        return text


def process_for_note(text, separator):

    filename = os.path.join(os.path.dirname(__file__), 'keywords.txt')

    with open(filename, 'r', encoding='utf-8') as f:
        keywords = f.read().splitlines()

    parts = text.split()
    result = ' '.join(v.upper() + '{}'.format(separator) if v in keywords else v for v in parts)
    result = result.replace(u'Δεν μου αρεσει', u'ΔΕΝ ΜΟΥ ΑΡΕΣΕΙ{}'.format(separator))
    result = result.replace(u'Νεανικα χρονια', u'ΝΕΑΝΙΚΑ ΧΡΟΝΙΑ{}'.format(separator))
    result = result.replace(u'Πρωτο ραντεβου', u'ΠΡΩΤΟ ΡΑΝΤΕΒΟΥ{}'.format(separator))
    result = result.replace(u'Κινητο τηλεφωνο', u'ΚΙΝΗΤΟ_ΤΗΛΕΦΩΝΟ{}'.format(separator))

    return result
