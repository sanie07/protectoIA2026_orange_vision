# 2D image-based detection of oranges and citrus fruit in orchards (state of the art to November 2026)

Evidence labels used on every finding:

- **[FT]** I read the full text directly (local PDF or a downloaded PDF, text extracted).
- **[FT-s]** Full page fetched, but read through an automated summariser, so figures passed through an intermediate step. Check the original before quoting.
- **[AB]** Abstract read verbatim through the OpenAlex record. Tables and methods not seen.
- **[AB-s]** Abstract seen only through a summariser (Europe PMC record).
- **[SN]** Search snippet only. Treat as a lead.
- **[SEC]** Figure reported by another paper, not checked in the original.

Metrics are almost never comparable across rows because datasets, labelling rules, IoU thresholds and hardware all differ. "mAP" without a threshold is what the paper printed; in most of these papers it appears to mean mAP@0.5, but several do not say so. Full citations are at the end of the last section.

## How did methods evolve from classical segmentation and ML to CNNs, YOLO variants and transformers?

### Takeaway
Citrus detection moved from colour and circle heuristics (about 50-90% recognition rates on small image sets) to Faster/Mask R-CNN and then to modified YOLO models, with YOLOv5 and YOLOv8 now the most common bases. RT-DETR variants have appeared since about 2025, but they do not consistently beat YOLO: the ranking reverses between datasets.

### Cited Findings

**Classical (pre-2018)**
- Plá et al. (1993): circular-feature citrus segmentation, recognition rate only 50% — [Tang 2020](https://doi.org/10.3389/fpls.2020.00510) [FT, SEC].
- Hannan et al. (2007): shape analysis plus an orange detection algorithm, more than 90% of fruit detected in 110 images — [Tang 2020](https://doi.org/10.3389/fpls.2020.00510) [FT, SEC].
- Bulanon et al. (2010), multispectral citrus: 88-93% recognition — [Tang 2020, Table 1](https://doi.org/10.3389/fpls.2020.00510) [FT, SEC].
- Kurtulmus et al. (2011), green citrus with eigenfruit, colour and circular Gabor texture: 75.3% recognition — [Tang 2020, Table 1](https://doi.org/10.3389/fpls.2020.00510) [FT, SEC]. Bibliographic record: [DOI](https://doi.org/10.1016/j.compag.2011.07.001).
- Illumination-adaptive segmentation tested on red litchi, purple grape and yellow citrus gave 93, 95 and 88% detection. Tang notes that colour segmentation alone fails when fruit and leaf colours are similar, so multi-feature fusion followed — [Tang 2020](https://doi.org/10.3389/fpls.2020.00510) [FT, SEC].
- Multi-feature fusion remained sensitive to light changes in natural environments, in the review's assessment — [Tang 2020](https://doi.org/10.3389/fpls.2020.00510) [FT].
- Wang et al. (2018/2019): LBP features on illumination-normalised images for immature green citrus. Metrics not retrieved — [record](https://doi.org/10.1007/s11119-018-9574-5) (metadata only).

**Early CNN and two-stage (2018-2022)**
- Liu et al. (2018): ResNet152 gave 95.35% recognition for citrus in natural environments and 97.86% for overlapping citrus (classification-style recognition, not box detection) — [Tang 2020](https://doi.org/10.3389/fpls.2020.00510) [FT, SEC].
- Wan & Goudos (2020): multi-class Faster R-CNN for orange, apple and mango, 90.72% mAP — [Hou 2022](https://doi.org/10.3389/fpls.2022.972445) [FT, SEC].
- He et al. (2020), deep bounding-box regression forest for immature citrus: mAP 87.60%, F1 85.38%, 0.759 s per image. VGG16 + Faster R-CNN (Xiong et al. 2018): mAP 85.49%, 0.400 s. Both as tabulated by [Zheng 2021](https://doi.org/10.3389/fpls.2021.705737) [FT-s, SEC]. Zheng's text and table disagree on the Faster R-CNN F1 (82.31 vs 85.31).
- Yang et al. (2020): Mask R-CNN on colour and depth images, AP 88.15% fruit and 96.27% branch; diameter errors 2.52 and 2.29 mm — [record](https://doi.org/10.1016/j.compag.2020.105469) [AB-s].
- Lu et al. (2022): Mask R-CNN with a CB-Net composite backbone for green citrus, AP50 95.36% and AP75 93.45% vs 94.03% and 92.17% baseline; about 0.94-0.97 s inference; 557 images and 3,273 instances — [Lu 2022](https://doi.org/10.3389/fpls.2022.946154) [FT-s].

**YOLOv3 to YOLOv5 (2021-2023)**
- OrangeYolo (YOLOv3-based, small-object scales, channel + spatial attention fusion): mAP 0.957 vs YOLOv3 0.905, YOLOv4 0.911, YOLOv5 0.917 — [Zhang W. 2022](https://doi.org/10.1093/hr/uhac003) [AB].
- YOLO BP (YOLOv4 with trimmed CSPDarknet and Bi-PANet), 890 green citrus images: mAP 91.55%, P 86%, R 91%, F1 88%, 18 FPS on GPU; YOLOv4 baseline 87.25% mAP, 17 FPS — [Zheng 2021](https://doi.org/10.3389/fpls.2021.705737) [FT-s].
- AC-YOLO (YOLOv4, panorama split into sub-images): P 96.19%, R 95.47%, AP 97.27%, gains of 1.07, 2.59 and 2.02 points over YOLOv4 — [Xu 2024](https://doi.org/10.4081/jae.2024.1654) [AB].
- YOLOv5-CS, green citrus: mAP@.5 98.23%, R 97.66%, P 86.97% — [Lyu 2022](https://doi.org/10.3390/s22020576) [FT-s].
- Improved YOLOv5s with a new loss, mature citrus: P 96.22%, R 98.85%, F1 0.98, 78.96 ms per frame on RTX 2080 — [Hou 2022](https://doi.org/10.3389/fpls.2022.972445) [FT].
- Lightweight green citrus, YOLOv5 with CNN-transformer backbone: 93.6% accuracy, 6.3 M parameters, 12.4 M model size, +1.5% vs YOLOv5s — [Lu 2023](https://doi.org/10.1016/j.compag.2023.108205) [AB-s].

**YOLOv7 to YOLOv11 (2024-2026)**
- YOLOv7-BiGS (XinHui and Emperor varieties, 400 original images): P 0.910, R 0.873, mAP@0.5 0.937, mAP@0.5:0.95 0.619 vs YOLOv7 0.852, 0.821, 0.889, 0.591. Parameters rose slightly (36.68 M vs 36.49 M). No FPS reported — [Deng 2024](https://doi.org/10.3389/fpls.2024.1381694) [FT-s].
- YOLO-PBGM (YOLOv7): P +0.3, R +4, mAP +3.5; parameters -15.4%, GFLOPs -23.7% — [Lv 2025](https://doi.org/10.3390/agriculture15101046) [AB].
- YCCB-YOLO (YOLOv8n, young citrus, 1,400 images): P 91.79%, R 92.75%, mAP 97.32%, 5.4 MB; YOLOv8 baseline 90.46, 90.51, 95.59 — [Ang 2024](https://doi.org/10.3389/fpls.2024.1375118) [FT-s]. The 97.32 figure does not appear in any of the paper's ablation tables.
- ORD-YOLO (YOLOv8, ripeness): P 93.83%, R 91.62%, mAP 96.92% — [Huang 2025](https://doi.org/10.3390/agriculture15151711) [FT-s of an abstract record].
- DC-YOLO (YOLOv8, 430 raw images, five ripeness classes): P 0.980, R 0.965, mAP50 0.975, mAP50:95 0.769, 9.82 M parameters, 93.42 FPS on RTX 4090. Baseline YOLOv8: mAP50 0.881, 80.59 FPS — [Zhang Q. 2026](https://doi.org/10.3389/fpls.2026.1911329) [FT-s].
- YOLO-MGP (YOLOv8n): P 94.2%, R 89.7%, mAP50 95.7% — [Yang 2026](https://doi.org/10.3390/horticulturae12060718) [AB]. Model size 4.4 MB [SN].
- OR-YOLOv11 (multi-ripeness): P 87.7%, R 79.8%, mAP@0.5 89.8%, 5.42 MB — [Xu L. 2026](https://doi.org/10.1016/j.atech.2026.102254) [AB].
- SEF-Net (YOLO11n, maturity): mAP@0.5 93.0%, 2.0 M parameters, 5.2 G, 4.3 MB, 132 FPS (hardware not given in the abstract) — [Fu 2026](https://doi.org/10.1088/2631-8695/ae9826) [AB].
- Systematic review of 90 YOLO-type citrus records (preprint): YOLOv8 and YOLOv5 each the base in about 22.2% of studies, YOLOv11 emerging from 2025; mean P 89.6%, R 85.9%, mAP@0.5 91.0% across fruit-level studies — [D'Antonio 2026](https://doi.org/10.21203/rs.3.rs-10773270/v1) [AB].

**Transformers**
- CitDet benchmark, tiled images: DETR AP 35.0, AP50 72.8; YOLOS 32.4, 70.7; Faster R-CNN 37.2, 76.0; YOLOv5 44.9, 81.9; YOLOv7 45.5, 83.1 — [James 2024](https://doi.org/10.1109/lra.2024.3474473) [FT].
- Oranges in the field benchmark: YOLOv11m mAP@0.5 0.892 vs RT-DETR 0.851. RT-DETR had higher recall, lower precision (more background false positives) and slower inference — [Carella 2026](https://doi.org/10.1016/j.compag.2026.111833) [FT]. The paper names YOLOv10x as best-performing but quotes the 0.892 for YOLOv11m, and YOLO11m is not in its listed model set.
- GeoSphere-DETR test set with cross-field and cross-day protocol: RGB-only RT-DETR mAP50 0.786 vs YOLOv11m 0.715; RGB-D GeoSphere-DETR 0.863 — [Liu 2026](https://doi.org/10.1016/j.aiia.2026.08.010) [AB].
- LightSal-RTDETR (ripeness): mAP@50 81%, +1.9 over the original, parameters -28.1%, computation -26.5% — [Huang Y. 2025](https://doi.org/10.3390/agronomy15051173) [AB].
- RT-DETR-DCEA (RT-DETR-R18, on-tree defective fruit, four classes): P 92.1%, R 86.1%, mAP@50 91.8%, about 14.77 M parameters, 81 FPS; authors note no edge-device validation — [Qiao 2026](https://doi.org/10.3390/plants15132077) [AB-s].
- LCWG-DETR (RT-DETR, fruit disease): JXDF mAP 98.24 vs 93.17 baseline; OFDD 96.28 vs 92.87; 19.74 M parameters, 92.45 FPS on RTX 4080 Super — [Zhang D. 2026](https://doi.org/10.3389/fpls.2026.1942627) [FT-s].
- MViTv2 backbone with Cascade Mask R-CNN for small green citrus was proposed in 2025; metrics not retrieved — [Smart Agricultural Technology paper](https://www.sciencedirect.com/science/article/pii/S277237552500067X) [SN].
- Egyptian orange benchmark (618 images): YOLOv11l segmentation mAP 0.932 at 26.1 ms per image, while RT-DETR gave the best total count in video (WMAPE 5.66%) despite the lowest static box accuracy — [Farhoud 2026](https://doi.org/10.1016/j.atech.2026.102529) [AB].

### Inferences
- The YOLO vs RT-DETR ordering depends on dataset and protocol: YOLO wins on Carella, RT-DETR wins on Liu's cross-field split. There is no general winner in citrus yet.
- Static mAP does not predict the downstream task. Farhoud's counting result shows this directly.
- Reported values are not a real timeline of progress: the 2022 YOLOv5-CS figure (98.23%) is above most 2026 figures, because of the dataset rather than the method.

### Gaps
- I found no citrus fruit paper based on YOLOv9 or using YOLOv12 as its main base. YOLOv12 appears only as a comparator in LCWG-DETR. YOLO26 appears only in non-citrus work ([Dimitrovski 2026](https://arxiv.org/abs/2609.13551), [AB-s]).
- Classical detail is thin. Search snippets mentioned a 2014 shape, texture and SVM method (80.4% detected) and a fast normalised cross-correlation plus Hough method (84.4% on 59 images), but I could not tie them to an opened record, so they are unverified.
- [Mirhaji 2021](https://doi.org/10.1016/j.compag.2021.106533) (YOLO on orange orchards under varied illumination, widely cited) could not be read; only its metadata was confirmed. Its metrics are a gap.

## Which architecture modifications are most common for citrus, and what gains do they report against which baselines?

### Takeaway
The common recipe combines attention, a lighter backbone or convolution, a P2 or small-object head, and an IoU-variant loss; half of YOLO citrus studies modify the architecture. Reported gains are usually 1-5 points of mAP against the unmodified parent model on the authors' own data. Augmentation and tiling can give larger gains than the modules do.

### Cited Findings

| Model (base) | Modules | Reported gain vs baseline | Data | Evidence |
|---|---|---|---|---|
| [YOLOv5-CS](https://doi.org/10.3390/s22020576) (YOLOv5s) | CBAM, 104×104 small-object layer, CIoU, cosine LR | Ablation mAP@.5: 96.66 base, 97.51 augmentation, 97.59 small layer, 98.05 CBAM | 2,831 images after augmentation | FT-s |
| [Hou 2022](https://doi.org/10.3389/fpls.2022.972445) (YOLOv5s) | Polarity BCE loss | Total R 98.85 vs 91.88; P 96.22 vs 95.56; F1 0.98 vs 0.94 | 4,855 image groups | FT |
| [YOLOv7-BiGS](https://doi.org/10.3389/fpls.2024.1381694) (YOLOv7) | BiFormer, GSConv | mAP@0.5 0.937 vs 0.889 | 400 originals | FT-s |
| [YOLO-PBGM](https://doi.org/10.3390/agriculture15101046) (YOLOv7) | PConv, BiFormer, GSConv, MPDIoU | R +4, mAP +3.5, parameters -15.4% | Own | AB |
| [YCCB-YOLO](https://doi.org/10.3389/fpls.2024.1375118) (YOLOv8n) | PConv + pointwise, Triplet, EMA, LSKA, SimSPPF | mAP +1.73, 5.4 MB | 1,400 images | FT-s |
| [YOLO-MGP](https://doi.org/10.3390/horticulturae12060718) (YOLOv8n) | MobileNetV3, C2f-GLU, P2 head, Coordinate Attention, PIoU | Baseline deltas not in abstract | Own | AB |
| [ORD-YOLO](https://doi.org/10.3390/agriculture15151711) (YOLOv8) | ODConv, RepGFPN, Dynamic Head, InnerDIoU | P +4.66, R +3.3, mAP +3 | Own | FT-s (abstract record) |
| [DC-YOLO](https://doi.org/10.3389/fpls.2026.1911329) (YOLOv8) | Dynamic depth-separable conv, collaborative attention, ripeness and visibility loss | mAP50 0.975 vs 0.881, parameters -12.79% | 430 originals | FT-s |
| [OR-YOLOv11](https://doi.org/10.1016/j.atech.2026.102254) (YOLOv11n) | RepConv Ghost CSPELAN, Deformable Attention, CGFPN | Deltas not in abstract | Own | AB |
| [MFAF-YOLO](https://doi.org/10.1016/j.compag.2024.108836) (YOLOv5s) | Adaptive multi-scale neck fusion | mAP 90.2, +3.8; 10.4 MB, -26.2% | Own | AB-s |
| [AG-YOLO](https://doi.org/10.3390/agriculture14010114) (NextViT) | Global Context Fusion Module (self-attention) | P 90.6, mAP@50 83.2, mAP@50:95 60.3, 34.22 FPS | 957 occlusion images | AB |
| [LDC-PP-YOLOE](https://dl.acm.org/doi/abs/10.1007/s10044-024-01329-1) (PP-YOLOE) | Localised knowledge distillation, CBAM | mAP@0.5 88%, mAP@0.95 51.3%, 8 M parameters | Own | SN |

- Half of the reviewed studies modified architecture, mainly attention modules, lightweight designs and IoU-loss variants. Original contributions concentrate in tracking, sensor fusion and yield modelling rather than the detector — [D'Antonio 2026](https://doi.org/10.21203/rs.3.rs-10773270/v1) [AB].
- Data handling can exceed module gains. Augmentation raised baseline AP from 71.31% to 92.47% in [Lu 2022](https://doi.org/10.3389/fpls.2022.946154) [FT-s], while the CB-Net backbone added 1.42 points.
- In CitDet, moving from whole images to tiles raised AP50 from 51.5 to 76.0 for Faster R-CNN and from 77.9 to 83.1 for YOLOv7 — [James 2024](https://doi.org/10.1109/lra.2024.3474473) [FT].
- Modified models can give up something unreported in the headline. YOLOv5-CS precision fell to 86.97% from 93.03% while mAP and recall rose — [Lyu 2022](https://doi.org/10.3390/s22020576) [FT-s]. YCCB-YOLO was slower than YOLOv8n on a CPU device (about 0.697 vs 0.656 s) — [Ang 2024](https://doi.org/10.3389/fpls.2024.1375118) [FT-s].
- Comparison tables can contradict the claim. DC-YOLO's own table shows Yolo-FD (0.987) and HPL-YOLOv4 (0.982) above its mAP50 of 0.975 and ORD-YOLO faster at 126.13 FPS — [Zhang Q. 2026](https://doi.org/10.3389/fpls.2026.1911329) [FT-s].

### Inferences
- In this sample, attention is close to universal, and BiFormer + GSConv recurs almost identically in two YOLOv7 papers (Deng 2024, Lv 2025). This count comes from my sample, not from a census.
- For a new project, tiling, augmentation and a suitable loss should be tried before custom attention blocks: in the ablations seen here, they give effects equal to or larger than the modules. Hou's loss alone added about 7 recall points.
- The 88.1 to 97.5 jump in DC-YOLO, on a test set derived by augmenting 430 raw images, should be read cautiously. If augmentation was done before splitting, near-duplicates could inflate results. The paper's order of operations was not checked.

### Gaps
- No controlled study was found that tests these modules across several citrus datasets, so which modules generalise is unknown.
- FPS and memory on the same hardware are rarely reported with the modules. Deng 2024 claims efficiency without FPS figures.

## How do methods deal with occlusion, clusters, variable lighting, green citrus on green foliage and small fruit? What about RGB-D, multispectral and thermal input?

### Takeaway
Most work stays RGB-only and handles these problems with attention, small-object heads, losses and augmentation, reporting results on the authors' own subsets. Depth is more often used for localisation than for detection, but 2026 RGB-D work shows a real false-positive reduction. Thermal and multispectral remain niche.

### Cited Findings

**Occlusion and clusters**
- AG-YOLO was evaluated on 957 images chosen for occlusion and overlap (mAP@50 83.2%), clearly lower than figures on general sets — [Lin 2024](https://doi.org/10.3390/agriculture14010114) [AB].
- YOLOv7-BiGS occlusion test: precision 0.991 vs YOLOv7 0.977, but on only 26 images — [Deng 2024](https://doi.org/10.3389/fpls.2024.1381694) [FT-s].
- Hou attributes misses to occluded fruit giving few features, and false alarms to immature citrus and yellow insect boards — [Hou 2022](https://doi.org/10.3389/fpls.2022.972445) [FT].
- Tracking reduces double counting of occluded fruit: OrangeSort MAE 0.081 vs Sort 0.45 and DeepSort 1.212 — [Zhang W. 2022](https://doi.org/10.1093/hr/uhac003) [AB].
- Annotation policy varies: Lu 2022 excluded fruit more than 70% occluded [FT-s](https://doi.org/10.3389/fpls.2022.946154); CitDet labelled all visible foreground fruit regardless of occlusion [FT](https://doi.org/10.1109/lra.2024.3474473); Hou labelled only fruit near the image centre [FT](https://doi.org/10.3389/fpls.2022.972445).

**Lighting**
- Hou 2022 recall by condition, new loss vs BCE: non-uniform 99.55 vs 90.47; weak 98.47 vs 91.91; good 98.48 vs 93.06 — [Hou 2022](https://doi.org/10.3389/fpls.2022.972445) [FT].
- Carella captured nine weather-lighting combinations and gives a YOLOv10x breakdown, but only in a figure — [Carella 2026](https://doi.org/10.1016/j.compag.2026.111833) [FT].
- Lightweight green citrus work uses a knowledge model to reconstruct blur — [Lu 2023](https://doi.org/10.1016/j.compag.2023.108205) [AB-s].

**Green citrus**
- Green-fruit models reporting high figures on their own data include YOLOv5-CS 98.23%, YCCB-YOLO 97.32%, Mask R-CNN + CB-Net AP50 95.36% and YOLO BP 91.55% (sources above). None tested on a shared set.
- Hou's detector of mature fruit confuses immature green citrus with mature fruit because shape and texture are similar — [Hou 2022](https://doi.org/10.3389/fpls.2022.972445) [FT].

**Small fruit**
- CitDet's mean object is about 50×50 pixels, less than 0.1% of the image. Small-object AP is far below the overall figure: YOLOv7 APS 19.2 vs AP 45.5 on tiles. Faster R-CNN has the best APS on both tiled and whole images (24.1 and 21.8) — [James 2024](https://doi.org/10.1109/lra.2024.3474473) [FT].
- Added high-resolution heads: 104×104 in YOLOv5-CS [FT-s](https://doi.org/10.3390/s22020576); P2 in YOLO-MGP [AB](https://doi.org/10.3390/horticulturae12060718). In YOLOv5-CS ablation the layer added only 0.08 points.
- Cropping helps. Carella's CUT-IMG + CLIP filtering improved all main metrics; the quoted 0.706 to 0.95 mean IoU applies to extreme examples only, not the whole test set — [Carella 2026](https://doi.org/10.1016/j.compag.2026.111833) [FT]. AC-YOLO splits panoramas into sub-images — [Xu 2024](https://doi.org/10.4081/jae.2024.1654) [AB].

**RGB-D, thermal, multispectral**
- GeoSphere-DETR (2,200 RGB-D images, 102,719 instances, cross-field and cross-day test): mAP50 0.863 and 3.29 false positives per image, vs RGB-only RT-DETR 0.786 and 7.24, and YOLOv11m 0.715 and 8.735. It uses curvature cues rather than raw depth — [Liu 2026](https://doi.org/10.1016/j.aiia.2026.08.010) [AB].
- NT-FFN: attention-based RGB-D fusion against depth noise, AP50 95.4% on its own citrus set at real-time speed — [Sun 2022](https://doi.org/10.1016/j.compag.2022.107034) [SN].
- Hou 2022 detects on RGB only and uses binocular depth (ZED 2) for localisation, with kriging to restore missing depth: 3.98 mm distance error — [Hou 2022](https://doi.org/10.3389/fpls.2022.972445) [FT].
- Colour + thermal fusion (CTCP algorithm): R 78.1-90.4%, P 86.6-95.5% — [Gan 2018](https://doi.org/10.1016/j.compag.2018.07.011) [AB-s]. A search summary attributed this to Faster R-CNN and Zheng 2021 calls it 95.5% accuracy; the abstract record supports neither wording.
- Active thermal imaging with water mist: mAP 87.2%, counting accuracy 96% — [Gan 2020](https://doi.org/10.1016/j.biosystemseng.2020.08.015) [AB-s].
- Thermal is sensitive to humidity, temperature and wind; hyperspectral cited at 80-89% (Okamoto & Lee 2009) and 96.97% (Torres 2019), but costs more — [Zheng 2021](https://doi.org/10.3389/fpls.2021.705737) [FT-s, SEC].
- The field still lacks multispectral data, according to the systematic review — [D'Antonio 2026](https://doi.org/10.21203/rs.3.rs-10773270/v1) [AB]. Campaneta-Orange-Fruit (2025) is a recent exception — [Zenodo](https://doi.org/10.5281/zenodo.17866344) [FT-s].
- Other fruit (context): RGB + NIR Faster R-CNN, DeepFruits — [Tang 2020](https://doi.org/10.3389/fpls.2020.00510) [FT, SEC]. Mask R-CNN on green persimmons: mAP 76.3 vs 73.2, small-object mAP 33.2 — [Jia 2022](https://doi.org/10.3389/fpls.2022.955256) [FT-s].

### Inferences
- GeoSphere-DETR is the strongest evidence for depth, because its protocol tests generalisation. Its benefit is mainly in false positives, which matters for a picking robot.
- For orange-coloured fruit near the camera, colour contrast is favourable, so the hard cases are occlusion and distance. Green citrus is harder, but published numbers do not show it because each paper uses a separate dataset.
- Occlusion results depend strongly on labelling rule, since excluding heavily occluded fruit removes the hardest cases from the metric.

### Gaps
- No paper was found that trains and tests the same detector across ripe and green citrus on a common protocol.
- No night-time citrus results were verified.
- I did not find benchmark results on Campaneta bands, so the value of NIR and red-edge for orange detection is unmeasured here.
- NT-FFN's dataset size and baseline numbers were not accessible.

## Which public datasets exist for citrus and orange detection, and how comparable are results across papers?

### Takeaway
Public citrus datasets now exist, mostly from 2024 onward, but no common benchmark has been adopted, and most papers still use private data. Results across papers cannot be compared: the same YOLOv11m scores 0.892 on one dataset and 0.715 on another.

### Cited Findings

| Dataset | Size | Modality and classes | Conditions | Access | Evidence |
|---|---|---|---|---|---|
| [CitDet](https://doi.org/10.1109/lra.2024.3474473) | 579 images (5,211 tiles); 460 train, 119 test | RGB 2448×3264; fruit on tree / on ground | Fort Pierce, Florida; HLB-affected; 60 varieties, 8 species; yield counts for 187 trees | Via [project site](https://robotic-vision-lab.github.io/citdet), MavMatrix, USDA | FT |
| [Oranges in the field](https://doi.org/10.17632/93f32zgkxz.1) | 5,025 tiles at 640×640 from 865 originals; 43,038 boxes | RGB; YOLO and COCO | Sicily; 7 phones; nine weather-light conditions | Mendeley, CC BY-NC 3.0 | FT, FT-s |
| [Campaneta-Orange-Fruit](https://doi.org/10.5281/zenodo.17866344) | 550 captures × 5 bands = 2,750; 301,232 instances (RGB 80,446) | UAV RGB + G, R, RE, NIR; YOLO format | Corbera, Valencia; 14 m altitude | Zenodo, CC BY 4.0 | FT-s |
| [citrus-fruit-rgbd](https://huggingface.co/datasets/ariel0818/citrus-fruit-rgbd) | 2,200 images (1,500/200/500); 102,719 instances | RGB + depth .npy, derived channels; 14.5 GB | Multiple orchards and days | Hugging Face, CC BY 4.0 | AB, FT-s |
| [Hou 2022](https://github.com/AshesBen/citrus-detection-localization) | 4,855 groups; 17,567 labelled fruit | ZED 2 RGB + depth, 1 class | Guangzhou hillside orchard; 30-150 cm; three illumination groups | GitHub with Drive link; the README still lists upload as to-do, so availability is uncertain | FT, FT-s |
| [Orange Fruit and Peduncle RGB-D](https://doi.org/10.5281/zenodo.23199294) | Counts not stated; about 3.8 GB | RGB-D; fruit and peduncle; includes weights | Fresno, California; navel | Zenodo, CC BY-SA 4.0 (Oct 2026) | FT-s |
| [OrangeFruitNet](https://doi.org/10.22266/ijies2025.1231.67) | Abstract says 7,000 images | RGB boxes; includes imagery from public sources | Mixed | [GitHub project](https://github.com/OrangeFruitNet-Project/) named in the paper; not opened | AB, partial FT |
| [CTSD](https://doi.org/10.57760/sciencedb.40726) | Counts not retrieved | Detection + segmentation, YOLO format | Citrus growth stages over 8 months, flowering to maturity | ScienceDB | AB |
| [OFDD](https://doi.org/10.3389/fpls.2026.1942627) | 700 images, 5 classes | Fruit disease, not plain detection | Described as public in LCWG-DETR | Not opened | FT-s |

- CitDet reports "over 32,000" annotations in its abstract but 44,233 in Table I, and an earlier search snippet said 600 images — [James 2024](https://doi.org/10.1109/lra.2024.3474473) [FT]. CitDet also lists Hou's data at 1,280×720, whereas Hou states 1920×1080 capture ([Hou 2022](https://doi.org/10.3389/fpls.2022.972445), [FT]).
- Context (not citrus), from the same table: MinneApple 1,001 images, 41,325 polygon annotations; Bargoti apple 841 images, 5,765 annotations — [James 2024](https://doi.org/10.1109/lra.2024.3474473) [FT].
- Only 13% of reviewed YOLO studies report mAP@0.5:0.95, and no individual metric is covered by much more than half. All but one study was rated at high risk of bias, largely for no statistical validation and limited dataset diversity. The authors conclude standardised benchmarks are missing — [D'Antonio 2026](https://doi.org/10.21203/rs.3.rs-10773270/v1) [AB, preprint].
- Same architecture, different numbers: YOLOv11m mAP50 0.892 on Oranges in the field [FT](https://doi.org/10.1016/j.compag.2026.111833) vs 0.715 on citrus-fruit-rgbd [AB](https://doi.org/10.1016/j.aiia.2026.08.010). YOLOv7 AP50 0.889 in [Deng 2024](https://doi.org/10.3389/fpls.2024.1381694) [FT-s] vs 83.1 (tiled) and 77.9 (whole) on CitDet [FT](https://doi.org/10.1109/lra.2024.3474473).
- Small or augmented test sets are common: Deng's test set grew from 40 to 297 images through augmentation [FT-s](https://doi.org/10.3389/fpls.2024.1381694); Ang's authors note overfitting risk on their small dataset [FT-s](https://doi.org/10.3389/fpls.2024.1375118).

### Inferences
- A mid-90s mAP@0.5 on a private set says little. CitDet's AP (IoU 0.5-0.95) of about 40-45 for YOLOv7 is a more sober picture of dense whole-tree scenes.
- A sensible protocol for this project: report mAP@0.5 and mAP@0.5:0.95, split by original image or orchard before augmenting or tiling, and test on at least one public dataset such as CitDet or Oranges in the field.
- Carella's 5,025 tiles come from 865 originals. Random splitting could leak scenes between train and test. I did not verify how the split was made, so check it before relying on the benchmark.
- For a project with oranges and a harvest-range camera, Oranges in the field (note the non-commercial licence) and citrus-fruit-rgbd are the most directly reusable. Campaneta fits only aerial work.

### Gaps
- Roboflow Universe and Kaggle citrus sets were not surveyed; many exist, with uncertain quality.
- CitDet's exact current licence terms, and the Drive contents of Hou's data, were not confirmed.
- I found no study that runs one model across multiple citrus datasets except OrangeFruitNet's cross-dataset section, which I only saw in part.

## Is there work on embedded and real-time deployment with measured FPS?

### Takeaway
Yes, but little for citrus fruit, and most "real-time" claims come from desktop GPUs. Verified citrus figures run from about 28 FPS on Jetson Xavier NX to single digits on Jetson Nano and 2-3 FPS on Raspberry Pi 4. I found no verified RT-DETR citrus fruit result on embedded hardware.

### Cited Findings

| Study | Fruit / model | Hardware | Measured speed | Evidence |
|---|---|---|---|---|
| [Lyu 2022](https://doi.org/10.3390/s22020576) | Green citrus, YOLOv5-CS, 416×416 | Jetson Xavier NX | 0.037 s per image; 28 FPS for detection + counting (YOLOv5s 0.04 s) | FT-s |
| [Khedkar 2025](https://doi.org/10.22266/ijies2025.1231.67) | Orange, YOLOv5s / YOLOv8n / YOLOv4 | Jetson Nano | 8 / 7 / 6 FPS | AB |
| [Khedkar 2025](https://doi.org/10.22266/ijies2025.1231.67) | Same | Raspberry Pi 4 | 2.5 / 2 / 3 FPS | AB |
| [Xu L. 2026](https://doi.org/10.1016/j.atech.2026.102254) | Citrus, OR-YOLOv11 on a harvesting robot | Device not named in abstract | 19.6 FPS, field recall 75.1% (79.8% offline) | AB |
| [Ang 2024](https://doi.org/10.3389/fpls.2024.1375118) | Young citrus, YCCB-YOLO | Intel Celeron J1900, 2 GB | About 0.697 s per image (about 1.4 FPS, my conversion) | FT-s |
| [Lu 2022](https://doi.org/10.3389/fpls.2022.946154) | Green citrus, Mask R-CNN | Jetson AGX Xavier used in the orchard | 0.939 or 0.969 s; paper does not state which hardware | FT-s |

- Desktop GPU figures for comparison: DC-YOLO 93.42 FPS on RTX 4090 [FT-s](https://doi.org/10.3389/fpls.2026.1911329); LCWG-DETR 92.45 on RTX 4080 Super [FT-s](https://doi.org/10.3389/fpls.2026.1942627); Hou 78.96 ms on RTX 2080 [FT](https://doi.org/10.3389/fpls.2022.972445).
- Hou cites 10-15 FPS as the minimum for picking robots (from Tu et al. 2020) — [Hou 2022](https://doi.org/10.3389/fpls.2022.972445) [FT].
- Authors acknowledge the gap: DC-YOLO did not measure Raspberry Pi performance [FT-s](https://doi.org/10.3389/fpls.2026.1911329); RT-DETR-DCEA reports no edge validation [AB-s](https://doi.org/10.3390/plants15132077); the systematic review finds rigorous field-deployment validation lacking [AB](https://doi.org/10.21203/rs.3.rs-10773270/v1).
- Citrus but not fruit: YOLO-Citrus (leaf disease) 51.5 FPS, 18.4 ms on Jetson Orin Nano 8 GB — [PMC12558917](https://pmc.ncbi.nlm.nih.gov/articles/PMC12558917/) [SN]. SKM-YOLOv11 on Jetson Orin NX Super, no FPS in the snippet — [Frontiers 2026](https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2026.1896487/full) [SN]. Citrus canopy segmentation 32.69 FPS on Xavier NX — [Xue 2023](https://doi.org/10.3390/agronomy13082059) [AB].
- Other fruit (context): YOLO26s on Jetson Orin Nano Super with TensorRT FP16: 66.76-74.56 images/s, full pipeline 44.96-54.11 FPS, FP16 mAP loss only 0.0020-0.0054, energy down about 64-66% — [Dimitrovski 2026](https://arxiv.org/abs/2609.13551) [AB-s]. Peach, MobileDet on Raspberry Pi + Coral TPU: AP 88.2%, 19.84 FPS at 640×480 — [Assunção 2022](https://doi.org/10.3390/fi14110323) [AB].
- Generic YOLOv7-tiny benchmark: Raspberry Pi 4B 0.9 FPS; Jetson Nano 7.4 and 5.2 FPS by power mode; Xavier NX at the 30 FPS camera cap — [IEEE paper](https://ieeexplore.ieee.org/iel8/9907/10705966/10705971.pdf) [SN].

### Inferences
- Hardware choice and export format matter more than the citrus-specific modules. TensorRT on Orin gives several times the speed of unoptimised Nano and Pi runs, although across different studies and fruits.
- For a harvesting robot's 10-15 FPS target, Xavier NX or Orin class hardware looks adequate, whereas a plain Raspberry Pi 4 does not, unless it has an accelerator such as a Coral TPU.
- Lightweight parameter counts do not guarantee faster embedded inference: YCCB-YOLO was smaller but slower than YOLOv8n on CPU. Attention and unusual convolutions may export or quantise poorly, though I found no citrus study measuring that.
- Lab-to-field loss is real but rarely measured: OR-YOLOv11 recall dropped 4.7 points on the robot.

### Gaps
- OrangeFruitNet's numbers need caution. Its abstract gives YOLOv8n the best mAP at 91.2%, while a table row extracted from the PDF shows YOLOv8-n at 93.1 and YOLOv5-s at 91.2. It also reports YOLOv4-Darknet53 faster than YOLOv8n on the Pi but slower on the Nano, which looks odd and which I could not explain. Export format was not confirmed.
- No quantised (INT8) citrus fruit results, and no power measurements for citrus, were found.
- No Orin-class citrus fruit detection FPS was verified, and the OR-YOLOv11 device remains unknown. [Ma 2026](https://doi.org/10.1016/j.compag.2026.111599) looks relevant, but no abstract or full text was accessible.
- MDPI, ScienceDirect and Springer blocked direct fetching, so results from those venues rest on abstracts and may omit embedded tests in the full text.

### Full citation list (all sections)

Author lists marked "et al." were truncated or inconsistent in the record seen.

- Ang G., Zhiwei T., Wei M., Yuepeng S., Longlong R., Yuliang F., Jianping Q., Xu L. (2024). Fruits hidden by green: an improved YOLOV8n for detection of young citrus in lush citrus trees. Frontiers in Plant Science 15:1375118. https://doi.org/10.3389/fpls.2024.1375118
- Assunção E. et al. (2022). Real-Time Image Detection for Edge Devices: A Peach Fruit Detection Application. Future Internet. https://doi.org/10.3390/fi14110323
- Bani Milhim A., Freire Bastidas D. M., Catalan A. (2026). Orange Fruit and Peduncle RGB-D Image Dataset for Robotic Citrus Harvesting. Zenodo. https://doi.org/10.5281/zenodo.23199294
- Carella A., Lucas B. P. E., El Ghazouali S., Bulacio Fischer P. T., Massenti R., Venturini F., Michelucci U., Lo Bianco R. (2026). Large-scale orange fruit dataset for localization, classification and ripening assessment under varying environments. Computers and Electronics in Agriculture 248:111833. https://doi.org/10.1016/j.compag.2026.111833
- D'Antonio P., Conceição L. A., Travascia D., Santana L. S., da Silva J. M., Toscano F. (2026). YOLO-Based Deep Learning for Citrus Fruit Detection, Counting, and Yield Estimation in Complex Orchard Environments: A Systematic Review. Research Square preprint, not peer reviewed. https://doi.org/10.21203/rs.3.rs-10773270/v1
- Deng F., Chen J., Fu L., Zhong J., Qiaoi W., Luo J., Li J., Li N. (2024). Real-time citrus variety detection in orchards based on complex scenarios of improved YOLOv7. Frontiers in Plant Science 15:1381694. https://doi.org/10.3389/fpls.2024.1381694
- Dimitrovski I., Spasev V., Kitanovski I., Lameski P., Boshev D. (2026). Towards Practical Precision Agriculture: Real-Time Fruit Detection and Video Analytics on Embedded Edge Hardware. arXiv:2609.13551. https://arxiv.org/abs/2609.13551
- Du J. (2026). CTSD-YOLO-Split: Citrus Time-Series Dataset for Object Detection and Segmentation. ScienceDB. https://doi.org/10.57760/sciencedb.40726
- Farhoud S. A., Zaghloul Y. A., Shehata O. M. (2026). Instance segmentation and multi-object tracking for fruit quality grading and dynamic yield estimation in Egyptian citrus orchards. Smart Agricultural Technology. https://doi.org/10.1016/j.atech.2026.102529
- Fu L. et al. (2026). ScaleEdgeFusion-Network: a lightweight and efficient model for citrus maturity detection in complex orchards. Engineering Research Express. https://doi.org/10.1088/2631-8695/ae9826
- Gan H., Lee W. S., Alchanatis V. (2018). Immature green citrus fruit detection using color and thermal images. Computers and Electronics in Agriculture 152:117-125. https://doi.org/10.1016/j.compag.2018.07.011
- Gan H., Lee W. S., Alchanatis V., Abd-Elrahman A. (2020). Active thermal imaging for immature citrus fruit detection. Biosystems Engineering. https://doi.org/10.1016/j.biosystemseng.2020.08.015
- Hou C., Zhang X., Tang Y., Zhuang J., Tan Z., Huang H., Chen W., Wei S., He Y., Luo S. (2022). Detection and localization of citrus fruit based on improved You Only Look Once v5s and binocular vision in the orchard. Frontiers in Plant Science 13:972445. https://doi.org/10.3389/fpls.2022.972445
- Huang Y., Wang X., Liu X., Cai L., Feng X., Chen X. (2025). A Lightweight Citrus Ripeness Detection Algorithm Based on Visual Saliency Priors and Improved RT-DETR. Agronomy. https://doi.org/10.3390/agronomy15051173
- Huang Z., Li X., Fan S., Liu Y., Zou H., He X., Xu S., Zhao J., Li W. (2025). ORD-YOLO: A Ripeness Recognition Method for Citrus Fruits in Complex Environments. Agriculture 15(15). https://doi.org/10.3390/agriculture15151711
- James J. A., Manching H. K., Mattia M. R., Bowman K. D., Hulse-Kemp A. M., Beksi W. J. (2024). CitDet: A Benchmark Dataset for Citrus Fruit Detection. IEEE Robotics and Automation Letters. https://doi.org/10.1109/lra.2024.3474473 (arXiv:2309.05645)
- Jia W., Wei J., Zhang Q., Pan N., Niu Y., Yin X., Ding Y., Ge X. (2022). Accurate segmentation of green fruit based on optimized mask RCNN application in complex orchard. Frontiers in Plant Science 13. https://doi.org/10.3389/fpls.2022.955256 (persimmon)
- Khedkar M., Sambhe V., Dhore V., Khedkar S., Khandare N. (2025). OrangeFruitNet: A Dataset and On-device Real Time YOLO-based Framework for Orange Fruit Detection and Yield Estimation in Orchard Environments. International Journal of Intelligent Engineering and Systems 18(11). https://doi.org/10.22266/ijies2025.1231.67
- Kurtulmus F., Lee W. S., Vardar A. (2011). Green citrus detection using 'eigenfruit', color and circular Gabor texture features under natural outdoor conditions. Computers and Electronics in Agriculture 78:140-149. https://doi.org/10.1016/j.compag.2011.07.001
- Lin Y., Huang Z., Liang Y., Liu Y., Jiang W. (2024). AG-YOLO: A Rapid Citrus Fruit Detection Algorithm with Global Context Fusion. Agriculture 14(1):114. https://doi.org/10.3390/agriculture14010114
- Liu S., Ampatzidis Y. G., Choi D., Lee W. W. (2026). GeoSphere-DETR: RGB-D citrus fruit detection in cluttered orchards via geometry-gated fusion and geometry-aware confidence recalibration. Artificial Intelligence in Agriculture. https://doi.org/10.1016/j.aiia.2026.08.010
- Lu J., Yang R., Yu C., Lin J., Chen W., Wu H., Chen X., Lan Y., Wang W. (2022). Citrus green fruit detection via improved feature network extraction. Frontiers in Plant Science 13:946154. https://doi.org/10.3389/fpls.2022.946154
- Lu J. et al. (2023). Lightweight green citrus fruit detection method for practical environmental applications. Computers and Electronics in Agriculture. https://doi.org/10.1016/j.compag.2023.108205
- Lucas B., Carella A., El Ghazouali S., Bulacio P., Massenti R., Venturini F., Michelucci U., Lo Bianco R. (2025). Oranges in the field. Mendeley Data. https://doi.org/10.17632/93f32zgkxz.1
- Lv Q., Sun F., Bian Y., Wu H., Li X., Li X. S., Zhou J. N. (2025). A Lightweight Citrus Object Detection Method in Complex Environments. Agriculture 15(10):1046. https://doi.org/10.3390/agriculture15101046
- Lyu S., Li R., Zhao Y., Li Z., Fan R., Liu S. (2022). Green Citrus Detection and Counting in Orchards Based on YOLOv5-CS and AI Edge System. Sensors 22(2):576. https://doi.org/10.3390/s22020576
- Ma J. et al. (2026). A generalization and lightweight recognition for citrus fruit harvesting based on improving YOLOv8. Computers and Electronics in Agriculture. https://doi.org/10.1016/j.compag.2026.111599 (metadata only)
- Mirhaji H., Soleymani M., Asakereh A., Mehdizadeh S. A. (2021). Fruit detection and load estimation of an orange orchard using the YOLO models through simple approaches in different imaging and illumination conditions. Computers and Electronics in Agriculture 191:106533. https://doi.org/10.1016/j.compag.2021.106533 (metadata only)
- Montalbán Faet G., Navarro Modesto E., Fayos-Jordan R., Benlloch-Caballero P., Salcedo Navarro A., Segura-Garcia J., Garcia Pineda M. (2025). Dataset for orange fruit detection from UAV in citrus orchards (Campaneta-Orange-Fruit). Zenodo. https://doi.org/10.5281/zenodo.17866344
- Qiao J., Sun Y., Zhong B., Wang L., Li S., Liu H., Chen Y., Li T. (2026). RT-DETR-DCEA: A Lightweight Citrus Defective Fruit Detection Algorithm for Complex Orchard Environments. Plants 15(13):2077. https://doi.org/10.3390/plants15132077
- Sun Q., Chai X., Zeng Z., Zhou G., Sun T. (2022). Noise-tolerant RGB-D feature fusion network for outdoor fruit detection. Computers and Electronics in Agriculture 198:107034. https://doi.org/10.1016/j.compag.2022.107034
- Tang Y., Chen M., Wang C., Luo L., Li J., Lian G., Zou X. (2020). Recognition and Localization Methods for Vision-Based Fruit Picking Robots: A Review. Frontiers in Plant Science 11:510. https://doi.org/10.3389/fpls.2020.00510
- Wan S., Goudos S. (2020). Faster R-CNN for multi-class fruit detection using a robotic vision system. Computer Networks 168:107036. https://doi.org/10.1016/j.comnet.2019.107036 (via Hou 2022)
- Wang C., Lee W. S., Zou X., Choi D., Gan H., Diamond J. (2018). Detection and counting of immature green citrus fruit based on the Local Binary Patterns (LBP) feature using illumination-normalized images. Precision Agriculture. https://doi.org/10.1007/s11119-018-9574-5 (metadata only)
- Xu L., Li H., Tang Z., He Y., Yu Y., Zi L., Jiang H., Wang Y. (2026). A multi-ripeness citrus detection model based on OR-YOLOv11. Smart Agricultural Technology. https://doi.org/10.1016/j.atech.2026.102254
- Xu X. H. et al. (2024). AC-YOLO: citrus detection in the natural environment of orchards. Journal of Agricultural Engineering. https://doi.org/10.4081/jae.2024.1654
- Xue X., Luo Q., Bu M., Li Z., Lyu S., Song S. (2023). Citrus Tree Canopy Segmentation of Orchard Spraying Robot Based on RGB-D Image and the Improved DeepLabv3+. Agronomy. https://doi.org/10.3390/agronomy13082059
- Yang C. H. et al. (2020). Integrated detection of citrus fruits and branches using a convolutional neural network. Computers and Electronics in Agriculture. https://doi.org/10.1016/j.compag.2020.105469
- Yang J., Wu H., Lv D., Ma W., Teng H., Chen D. (2026). A Lightweight and High-Precision Citrus Detection Model for Unstructured Orchard Environments. Horticulturae 12(6):718. https://doi.org/10.3390/horticulturae12060718
- Zhang D., Wu B., Gao K., Yan G. (2026). LCWG-DETR: a wavelet-enhanced detection transformer for citrus disease detection improving visual perception in harvesting. Frontiers in Plant Science 17. https://doi.org/10.3389/fpls.2026.1942627
- Zhang Q., Hang Y., Zhang Y., Gao D., Wang S. (2026). An effective citrus ripeness detection model for complex orchard scenarios. Frontiers in Plant Science 17:1911329. https://doi.org/10.3389/fpls.2026.1911329
- Zhang W., Wang J., Liu Y., Chen K., Li H., Duan Y., Wu W., Shi Y. (2022). Deep-learning-based in-field citrus fruit detection and tracking. Horticulture Research. https://doi.org/10.1093/hr/uhac003
- Zhang Y., Li L., Chun C., Wen Y., Xu G. (2024). Multi-scale feature adaptive fusion model for real-time detection in complex citrus orchard environments. Computers and Electronics in Agriculture 219:108836. https://doi.org/10.1016/j.compag.2024.108836
- Zheng Z., Xiong J., Lin H., Han Y., Sun B., Xie Z., Yang Z., Wang C. (2021). A Method of Green Citrus Detection in Natural Environments Using a Deep Convolutional Neural Network. Frontiers in Plant Science 12:705737. https://doi.org/10.3389/fpls.2021.705737
