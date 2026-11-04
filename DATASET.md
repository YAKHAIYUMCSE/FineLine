# Dataset

**Product:** FineLine (E-CIT-07) · **Owner:** Ya Khaiyum A
**Source:** India Code (indiacode.gov.in), the official Government of India legislation portal
**Licence / terms:** India Code Copyright Policy (updated 22 Jun 2026) read on 1 Nov 2026. Content is owned by the Legislative Department, Ministry of Law and Justice. Only limited personal, non-commercial use for research and study is permitted, with the source cited as "IndiaCode Portal, Legislative Department, Ministry of Law and Justice, Government of India". Used here only for a learning project; one copy downloaded manually; the PDF is not redistributed.
**How to rebuild:** download the PDF manually from the link in `urls.txt`, then run `python tools/count_pages.py`

| Files | Pages | Date range | Downloaded on |
|---|---|---|---|
| 1 PDF | 176 | text as on 15 Aug 2026 | 1 Nov 2026 |

| File | Source URL | Pages | Notes |
|---|---|---|---|
| indiacode_2026-08-15_motor-vehicles-act-1988.pdf | https://indiacode.gov.in/pdf-viewer/2bbbcc40-38f1-4b15-ae94-646b85db4ee7/031fe0a8-b3a6-4da2-b130-ec2e870fe4f2 | 176 | current consolidated text; amending Acts still to be added |

Sample in data/sample/: 1 file (the Motor Vehicles Act PDF, one copy, committed with the trainer's approval on 1 Nov 2026). Full data in data/raw/ (not in Git).

## Open issues
- Old links on indiacode.nic.in gave an Akamai (edgesuite) error and are blocked by robots.txt for scripts, so the PDF was downloaded manually in a browser from indiacode.gov.in.
- Still to collect: the Motor Vehicles (Amendment) Act 2019 and other amending Acts (needed for dated versions), MoRTH accident reports, Tamil Nadu Transport Department notes.
- India Code's Copyright Policy restricts redistribution. Only one sample PDF is committed, with trainer approval, for a learning project. No other India Code files are redistributed.
- No personal data in the documents.
