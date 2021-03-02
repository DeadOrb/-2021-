def get_probs(alphabet, text):
    probs = [0] * len(alphabet)
    for i, a in enumerate(alphabet):
        probs[i] = text.count(a) / len(text)
    return probs

def define_segments(alphabet, probs):
    segments = dict()
    l = 0
    for i, c in enumerate(alphabet):
        left = l
        right = l + probs[i]
        segments[c] = (left, right) # left border, right border
        l = right
    return segments

def ariphmetic_encode(alphabet, probs, text): 
    segments = define_segments(alphabet, probs)
    # print(segments)
    left = 0
    right = 1
    for i, letter in enumerate(text):
        left, right  = left + (right - left) * segments[letter][0], left + (right - left) * segments[letter][1]
        # print(left, right)
    return (left + right) / 2

def define_segments2(alphabet, probs):
    segments = []
    l = 0.0
    for i, c in enumerate(alphabet):
        left = l
        right = l + probs[i]
        segments[c] = (left, right) # left border, right border, alphabet[i]
        l = right
        return segments

def ariphmetic_decode(alphabet, probs, code, text_len, segments):
    segments = define_segment2(alphabet, probs)
    res = []
    for i in range(text_len):
        for segm in segments:
            left, right = segments
    
    return ''.join(res)
