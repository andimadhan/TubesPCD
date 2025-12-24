# Image Compression using DCT, Quantization, and Huffman Entropy (Python)

---

## Fitur Utama
- Discrete Cosine Transform (DCT) blok 8×8
- Quantization matrix dengan parameter kualitas (quality)
- Rekonstruksi citra menggunakan Inverse DCT
- Visualisasi error menggunakan **Heatmap**
- Estimasi **entropy & ukuran bitstream Huffman**
- Mendukung citra **RGB (3 channel)**

---

## Library yang Digunakan
- `opencv-python`
- `numpy`
- `scipy`
- `collections`
- `math`

---

## Alur Kompresi
1. Membaca citra RGB
2. Memisahkan channel **R, G, B**
3. Membagi citra menjadi blok **8×8**
4. Menghitung **DCT** pada setiap blok
5. Melakukan **Quantization**
6. Rekonstruksi citra dengan **Inverse DCT**
7. Menggabungkan kembali channel
8. Menyimpan hasil kompresi
9. Menghitung **heatmap error**
10. Mengestimasi **entropy Huffman**

---

## Output
Fungsi `compress_image()` menghasilkan:
- `result.jpeg` → citra terkompresi
- `heatmap.png` → visualisasi error
- Entropy Huffman
- Estimasi ukuran data (KB)

---

## Catatan Penting
- Proyek ini **tidak mengimplementasikan JPEG encoder penuh**
- Huffman coding hanya dihitung sebagai **estimasi statistik**
- OpenCV digunakan **hanya untuk penyimpanan file**

---

## 📎 Lisensi
Bebas digunakan untuk keperluan edukasi dan penelitian.