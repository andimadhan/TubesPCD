import cv2
import numpy as np
from scipy.fftpack import dct, idct
from collections import Counter
import heapq
import math

# ================= DCT HELPERS =================
def dct2(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

def idct2(block):
    return idct(idct(block.T, norm='ortho').T, norm='ortho')

def scale_quant_matrix(Q, quality):
    if quality < 50:
        scale = 50 / quality
    else:
        scale = 2 - (quality / 50)
    return np.clip(np.round(Q * scale), 1, 255)

# ================= HUFFMAN =================
def huffman_entropy(data):
    freq = Counter(data)
    total = sum(freq.values())

    entropy = 0
    for count in freq.values():
        p = count / total
        entropy -= p * math.log2(p)

    # estimasi ukuran bitstream Huffman
    bits = entropy * total
    return entropy, bits

# ================= CHANNEL COMPRESSION =================
def compress_channel(channel, Q):
    h, w = channel.shape
    out = np.zeros((h, w), np.float32)
    coeffs = []

    for i in range(0, h, 8):
        for j in range(0, w, 8):
            block = channel[i:i+8, j:j+8]
            if block.shape != (8, 8):
                continue

            d = dct2(block)
            q = np.round(d / Q)

            coeffs.extend(q.flatten())
            out[i:i+8, j:j+8] = idct2(q * Q)

    return out, coeffs

# ================= MAIN =================
def compress_image(image_path, quality):
    img = cv2.imread(image_path)
    img = np.float32(img)

    b, g, r = cv2.split(img)

    base_Q = np.array([
        [16,11,10,16,24,40,51,61],
        [12,12,14,19,26,58,60,55],
        [14,13,16,24,40,57,69,56],
        [14,17,22,29,51,87,80,62],
        [18,22,37,56,68,109,103,77],
        [24,35,55,64,81,104,113,92],
        [49,64,78,87,103,121,120,101],
        [72,92,95,98,112,100,103,99]
    ])

    Q = scale_quant_matrix(base_Q, quality)

    b_c, b_coeff = compress_channel(b, Q)
    g_c, g_coeff = compress_channel(g, Q)
    r_c, r_coeff = compress_channel(r, Q)

    compressed = cv2.merge([
        np.clip(b_c, 0, 255).astype(np.uint8),
        np.clip(g_c, 0, 255).astype(np.uint8),
        np.clip(r_c, 0, 255).astype(np.uint8)
    ])

    result_path = "static/result.jpeg"
    cv2.imwrite(result_path, compressed)

    # ================= HEATMAP =================
    error = cv2.absdiff(img.astype(np.uint8), compressed)
    error_gray = cv2.cvtColor(error, cv2.COLOR_BGR2GRAY)

    heatmap = cv2.applyColorMap(
        cv2.normalize(error_gray, None, 0, 255, cv2.NORM_MINMAX),
        cv2.COLORMAP_JET
    )

    heatmap_path = "static/heatmap.png"
    cv2.imwrite(heatmap_path, heatmap)

    # ================= HUFFMAN STATS =================
    all_coeffs = np.concatenate([b_coeff, g_coeff, r_coeff])
    entropy, total_bits = huffman_entropy(all_coeffs)

    return result_path, heatmap_path, entropy, round(total_bits / 8 / 1024, 2)