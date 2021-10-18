HIRA = 'あいうえおかきくけこさしすせそたちつてと' \
       'なにぬねのはひふへほまみむめもやゆよ' \
       'らりるれろわをんがぎぐげござじずぜぞ' \
       'だぢづでどばびぶべぼぱぴぷぺぽ' \
       'ぁぃぅぇぉゃゅょっゎゐゑかか'
KATA = 'アイウエオカキクケコサシスセソタチツテト' \
       'ナニヌネノハヒフヘホマミムメモヤユヨ' \
       'ラリルレロワヲンガギグゲゴザジズゼゾ' \
       'ダヂヅデドバビブベボパピプペポ' \
       'ァィゥェォャュョッヮヰヱヵヶ'

hira_kana_map = {HIRA[i]: KATA[i] for i in range(len(HIRA))}
kata_hira_map = {KATA[i]: HIRA[i] for i in range(len(KATA))}


def get_tone(tone):
    if isinstance(tone, float):
        return '(%s)' % str(int(tone))
    if tone == '':
        return ''
    if '(' in tone:
        return tone
    else:
        tones = []
        for t in str.split(tone, ' '):
            tones.append('(%s)' % t)
        return str.join('', tones)


def get_part(part):
    if '[' in part:
        return part
    return '[' + str.replace(part, ' ', '·') + ']'


def hira_to_kata(hira):
    kana = map(lambda h: hira_kana_map[h] if h in hira_kana_map else h, hira)
    return str.join('', kana)


def kata_to_hira(kata):
    hira = map(lambda k: kata_hira_map[k] if k in kata_hira_map else k, kata)
    return str.join('', hira)
