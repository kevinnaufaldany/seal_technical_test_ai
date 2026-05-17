from pathlib import Path
from typing import Any


def get_visual_knowledge(source_file: str) -> list[dict[str, Any]]:
    """
    Curated visual knowledge from charts / infographics in the PDF.

    Tujuan:
    - Membantu RAG memahami informasi dari chart dan infografis.
    - Informasi ini tetap diberi metadata halaman.
    - Ini bukan hardcode jawaban endpoint, tetapi hasil interpretasi visual
      yang ikut masuk ke vector database seperti dokumen biasa.
    """

    return [
        {
            "content": """
Halaman 4 - Tabel Kredit yang Diberikan dan Piutang/Pembiayaan Syariah Berdasarkan Sektor Ekonomi.

Tabel ini menjelaskan nilai kredit berdasarkan sektor ekonomi tahun 2024 dan 2025, beserta pertumbuhan nominal dan persentasenya.

Data penting:
- Industri: 2024 Rp198.299.361 juta, 2025 Rp217.086.468 juta, pertumbuhan Rp18.787.107 juta atau 9,47%.
- Perdagangan, Restoran dan Hotel: 2024 Rp180.565.431 juta, 2025 Rp203.653.075 juta, pertumbuhan Rp23.087.644 juta atau 12,79%.
- Pertanian: 2024 Rp156.305.561 juta, 2025 Rp203.989.473 juta, pertumbuhan Rp47.683.912 juta atau 30,51%.
- Jasa Dunia Usaha: 2024 Rp146.987.732 juta, 2025 Rp139.875.667 juta, pertumbuhan negatif Rp7.112.065 juta atau -4,84%.
- Tambang: 2024 Rp145.571.176 juta, 2025 Rp157.186.029 juta, pertumbuhan Rp11.614.853 juta atau 7,98%.
- Pengangkutan, Pergudangan dan Komunikasi: 2024 Rp126.768.881 juta, 2025 Rp153.068.816 juta, pertumbuhan Rp26.299.935 juta atau 20,75%.
- Konstruksi: 2024 Rp99.883.788 juta, 2025 Rp108.148.636 juta, pertumbuhan Rp8.264.848 juta atau 8,27%.
- Jasa Sosial: 2024 Rp106.464.061 juta, 2025 Rp138.540.617 juta, pertumbuhan Rp32.076.556 juta atau 30,13%.
- Listrik, Gas dan Air: 2024 Rp62.035.505 juta, 2025 Rp97.973.432 juta, pertumbuhan Rp35.937.927 juta atau 57,93%.
- Lain-lain: 2024 Rp400.335.116 juta, 2025 Rp430.445.743 juta, pertumbuhan Rp30.110.627 juta atau 7,52%.
- Jumlah: 2024 Rp1.623.216.612 juta, 2025 Rp1.849.967.956 juta, pertumbuhan Rp226.751.344 juta atau 13,97%.
""".strip(),
            "metadata": {
                "source_file": source_file,
                "page": 4,
                "content_type": "visual_table_caption",
                "visual_title": "Kredit yang Diberikan Berdasarkan Sektor Ekonomi",
            },
        },
        {
            "content": """
Halaman 6 - Chart Komposisi DPK Bank Mandiri.

Chart ini menampilkan komposisi Dana Pihak Ketiga atau DPK Bank Mandiri untuk tahun 2024 dan 2025.

Kategori chart:
- Giro dan Giro Wadiah
- Tabungan dan Tabungan Wadiah
- Deposito Berjangka

Komposisi DPK tahun 2024:
- Giro dan Giro Wadiah: 39,31%.
- Tabungan dan Tabungan Wadiah: 40,12%.
- Deposito Berjangka: 20,57%.

Komposisi DPK tahun 2025:
- Giro dan Giro Wadiah: 36,66%.
- Tabungan dan Tabungan Wadiah: 34,23%.
- Deposito Berjangka: 29,11%.

Interpretasi:
- Porsi deposito berjangka meningkat dari 20,57% pada 2024 menjadi 29,11% pada 2025.
- Porsi tabungan dan tabungan wadiah turun dari 40,12% pada 2024 menjadi 34,23% pada 2025.
- Porsi giro dan giro wadiah turun dari 39,31% pada 2024 menjadi 36,66% pada 2025.
""".strip(),
            "metadata": {
                "source_file": source_file,
                "page": 6,
                "content_type": "visual_chart_caption",
                "visual_title": "Komposisi DPK Bank Mandiri",
            },
        },
        {
            "content": """
Halaman 8 - Infografis Penanganan Pengaduan Nasabah.

Infografis ini menjelaskan alur penanganan pengaduan nasabah Bank Mandiri.

Alur penanganan pengaduan nasabah:
1. Nasabah menyampaikan pengaduan.
2. Pengaduan dapat disampaikan melalui media masa, telepon, email, media sosial, surat, atau cabang.
3. Bank menerima pengaduan dan melakukan verifikasi.
4. Pengaduan diinput ke dalam sistem pengaduan.
5. Bank melakukan investigasi.
6. Bank membuat keputusan.
7. Update hasil investigasi dimasukkan ke dalam sistem pengaduan.
8. Bank menginformasikan hasil investigasi kepada nasabah.
9. Nasabah menerima hasil pengaduan.

Kata kunci visual:
- Menyampaikan pengaduan
- Media masa
- Telepon
- Email
- Media sosial
- Surat
- Cabang
- Menerima pengaduan dan verifikasi
- Input pengaduan
- Melakukan investigasi
- Membuat keputusan
- Sistem pengaduan
- Update hasil investigasi
- Menginfokan hasil investigasi kepada nasabah
- Menerima hasil pengaduan
""".strip(),
            "metadata": {
                "source_file": source_file,
                "page": 8,
                "content_type": "visual_infographic_caption",
                "visual_title": "Penanganan Pengaduan Nasabah",
            },
        },
        {
            "content": """
Halaman 9 - Gambar Daftar Saluran Pengaduan Bank Mandiri.

Gambar ini menjelaskan saluran pengaduan yang disediakan Bank Mandiri agar nasabah dapat menyampaikan keluhan secara lisan maupun tertulis.

Saluran pengaduan Bank Mandiri:
1. Mandiri Call layanan 14000.
2. Akun X: mandiricare dan @bankmandiri.
3. WhatsApp MITA 24 jam melalui nomor 0811-8414-000.
4. Website www.bankmandiri.co.id dengan memilih menu contact us.
5. Akun Facebook "Mandiri Care" dan "Bank Mandiri".
6. Kantor cabang Bank Mandiri di seluruh Indonesia.
7. Email mandiricare@bankmandiri.co.id.
8. Akun Instagram @bankmandiri.
9. Surat resmi yang ditujukan kepada Bank Mandiri, baik diantar langsung maupun dikirim melalui pos.

Selain itu, Bank Mandiri juga menyediakan saluran pelaporan Whistleblowing System - Letter to CEO atau WBS-LTC yang dikelola oleh pihak ketiga independen.
""".strip(),
            "metadata": {
                "source_file": source_file,
                "page": 9,
                "content_type": "visual_infographic_caption",
                "visual_title": "Daftar Saluran Pengaduan Bank Mandiri",
            },
        },
    ]