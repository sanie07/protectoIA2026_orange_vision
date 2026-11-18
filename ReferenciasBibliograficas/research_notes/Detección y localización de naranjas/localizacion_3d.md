# 3D localization of oranges and citrus fruit from vision sensors in orchards

Notes compiled 2026-11-04. Coverage runs to the search date, with priority on 2018 onward. Older papers are dated and included only where they supply baseline numbers.

**Verification tags on every figure:**
- **[FULL]**: I read the paper's text (local PDF, or arXiv PDF converted to text).
- **[FETCH]**: full text read through a web extraction tool, so the values are one step removed. Re-check before quoting.
- **[ABS]**: abstract only (publisher abstract via OpenAlex or arXiv).
- **[SNIP]**: search-result snippet or summary only. Treat as a lead, not a verified figure.
- **[VIA x]**: reported by paper x about another paper. The original was not read.

MDPI, ScienceDirect and Bohrium pages returned 403 or WAF blocks to my tools, so several MDPI and Elsevier papers are [ABS] or [SNIP] only.

**Errors are not comparable across studies.** They differ in target point (visible surface, geometric centre, picking point, stem), metric (mean signed error, MAE, RMSE, SD, Euclidean), axis (depth only or 3D), reference (laser rangefinder, motion capture, checkerboard, self-reference) and scene (lab or orchard).

## What sensing approaches are used?

### Takeaway
Consumer RGB-D cameras (mostly RealSense D400 active stereo) and passive stereo (ZED) dominate citrus work, and ToF plus solid-state LiDAR give the best evidence for sunlit, 1.5–2 m operation, but mainly on apples. I found no citrus study reporting mm-level 3D fruit error for LiDAR fusion, ToF, NeRF or Gaussian splatting, and no metric citrus result for Depth Anything or MiDaS.

### Cited Findings

**Passive stereo**
- **Citrus, orchard (Hou 2022) [FULL]:** ZED 2 at 1920×1080, 30–150 cm, 'Shantanju' citrus in a Guangzhou hillside orchard, sunny and cloudy, December 2020 and 2021. Average camera-to-fruit distance error 3.98 mm against a laser rangefinder (UNI-T UT392B), on 22 images only — [Hou et al. 2022](https://doi.org/10.3389/fpls.2022.972445).
- **Citrus picking point (Hou 2024) [SNIP]:** binocular vision, MAE 8.63 mm, MRE 2.76%. Citation confirmed through Crossref, but the figures come from a snippet — [Hou et al. 2024](https://doi.org/10.1007/s11119-024-10169-2).
- **Orange, historical (Plebe & Grasso 2001) [VIA Tang 2020]:** stereo cameras on each arm of an orange harvester, matching orange centres of mass. The review gives no error figure — [Tang et al. 2020](https://doi.org/10.3389/fpls.2020.00510).
- **Apple and pear, lab (Font 2014) [FULL], other fruit:** Minoru webcam, 60 mm baseline, 800×600, centroid matching, 203–2025 mm, white background. Calibrated apple distance error (mean/SD) was 21.16/4.29 mm at 977 mm and 65.14/24.93 mm at 2025 mm. Uncalibrated at 2025 mm it was 288.93/174.68 mm. Authors describe about 4% average distance error — [Font et al. 2014](https://doi.org/10.3390/s140711557).
- **Apple under canopy (Si 2015) [VIA Tang 2020], other fruit:** errors below 20 mm at 400–1500 mm — [Tang et al. 2020](https://doi.org/10.3389/fpls.2020.00510).

**Active stereo, ToF and structured light (RGB-D)**
- **Camera benchmark for orchards (Neupane 2021) [ABS], tested on fruit-sizing use, fruit not specified in the abstract:** eight cameras: ZED, ZED2, OAK-D (stereo); D435 (IR active stereo); L515, Kinect v2, Blaze 101, Azure Kinect (ToF). The specification was bias-corrected RMSE of 20 mm at 2 m in sunlit field conditions. The ToF cameras met it, and Blaze 101 or Azure Kinect were recommended. Azure Kinect at 1.5 m in sunlight: RMSE 6 mm, bias 17 mm, SD 2 mm, fill rate 100% on a central 50×50 pixel patch — [Neupane et al. 2021](https://doi.org/10.3390/agronomy11091780).
- **Kiwifruit calyx, orchard (Liu 2024) [ABS], other fruit, non-spherical target:** Azure Kinect, D435 and ZED 2i compared. Mean absolute deviation on Y was 8.44 mm (ZED 2i) and 6.67 mm (Azure Kinect). D435 had the minimum on X (10.42 mm) and Z (18.33 mm). Authors favour D435, which also had the fastest localization at 0.037 s per image — [Liu et al. 2024](https://doi.org/10.1002/rob.22297). This ranking conflicts with Neupane's, under different lighting, range and target.
- **Tabletop benchmark (Rustler 2025) [ABS]:** D435 error under 1 cm up to about 1 m in all tested scenarios. ZED 2 error under 3 cm at 4 m and rated best overall, but needs a GPU — [Rustler et al. 2025](https://arxiv.org/abs/2501.07421).
- **Citrus field systems:** see the citrus table under the last question. Most report recognition or picking success, not coordinate error.

**Manufacturer specifications** (depth noise only, not fruit localization)
- **Azure Kinect [FULL]:** ToF, 0.25–5.46 m depending on mode, random error SD ≤17 mm, typical systematic error <11 mm + 0.1% of distance without multipath, rated for 10–25 °C ambient — [Microsoft archived specification](https://learn.microsoft.com/en-us/previous-versions/azure/kinect-dk/hardware-specification).
- **RealSense D435i [VIA Zhang 2023]:** datasheet accuracy <2% of depth range, which those authors convert to <24 mm at 0.6–1.2 m. This is an estimate from the datasheet, not a measurement — [Zhang et al. 2023](https://arxiv.org/abs/2311.02500).
- **RealSense D455 [FETCH, via Kang 2022]:** 0.6–6 m, ≤2% over 0.6–4 m — [Kang et al. 2022](https://ar5iv.labs.arxiv.org/html/2205.00404).
- **ZED 2i [FETCH]:** 120 mm baseline, 0.3–20 m with 2.1 mm lens. The product page gives no depth accuracy figure — [Stereolabs](https://www.stereolabs.com/en-us/products/zed-2).
- **ZED 2 secondary figures conflict [SNIP]:** one paper's table says <0.8% at 2 m and its text says <2% at 4 m — [Rustler et al. 2025 PDF](https://arxiv.org/pdf/2501.07421).
- **Percipio TL460-S1-E1 ToF [FULL, via Zhu 2026]:** 0.3–9.5 m, ±4 mm + 0.25% of range — [Zhu et al. 2026](https://arxiv.org/pdf/2606.14089).
- **TuYang TM460-E2 ToF [FETCH]:** 0.1–2.4 m, authors state Z accuracy 5–20 mm — [Zhang et al. 2023 hand-eye](https://doi.org/10.3389/fpls.2022.1099033).

**LiDAR and camera-LiDAR fusion (no citrus result found)**
- **Livox Mid-70 + D455 RGB, apple orchard (Kang 2022) [FETCH], other fruit:** standard deviation of location estimates, in cm, against D455 depth at the same range. The reported SD is repeatability, because no independent ground truth is described. Conclusion text misstates the unit as m; table and abstract use cm — [Kang et al. 2022](https://ar5iv.labs.arxiv.org/html/2205.00404).

| Range (m) | LiDAR-RGB SD (cm) | D455 SD (cm) |
|---|---|---|
| 0.5 | 0.245 | 1.006 |
| 0.8 | 0.236 | 1.051 |
| 1.2 | 0.227 | 1.175 |
| 1.5 | 0.204 | 1.238 |
| 1.8 | 0.275 | 1.360 |

**Laser triangulation (other fruit)**
- **ALACS on checkerboard (Zhang 2023) [FULL]:** line laser + RGB camera + linear slide. Typically within 0.4, 0.8 and 3 mm (x, y, z), maximum under 0.6, 1.2 and 4 mm, at 0.6–1.2 m on a planar checkerboard — [Zhang et al. 2023](https://arxiv.org/abs/2311.02500).
- **ALACS on apples (Chu 2023) [ABS]:** average 6.9–11.2 mm at 1.0–1.6 m against 21.5 mm for RealSense, indoors. In orchard evaluations, fruit detachment was 95% against 71% — [Chu et al. 2023](https://arxiv.org/abs/2311.08674).
- **Citrus laser ranging, historical (Jimenez 1999) [VIA Tang 2020]:** IR laser range sensor for 3D position and radius of spherical fruit, 80–90% detection on citrus. Tang also lists structured-light drawbacks: blocked beam, defocus at range, added system complexity — [Tang et al. 2020](https://doi.org/10.3389/fpls.2020.00510).

**Monocular**
- **Citrus, learned depth (Kong 2023) [ABS]:** fused multi-resolution monocular depth with YOLOv8s. At 30–60 cm the abstract gives MAE 0.53 and RMSE 0.53 with **no units**, and at 1000–5000 lx gives 0.49 and 0.64. Grasp success in a simulated picking scene was 80.6% at 30 cm and 85.1% at 45 cm. Authors claim independence from camera parameters and fruit size, a limit of monocular geometric methods — [Kong et al. 2023](https://doi.org/10.3390/agronomy13082122).
- **Citrus, moving monocular triangulation (Mehta & Burks 2014) [VIA Kang 2022]:** camera motion-based triangulation, overall controller accuracy about 15 mm — [Mehta & Burks 2014](https://doi.org/10.1016/j.compag.2014.01.003).
- **Citrus, monocular pose (Xiao 2024) [ABS]:** recognition and positioning success 93.6%, mean attitude error 7.9°, field picking success 85.1%, 5.6 s per fruit. No mm position error in the abstract — [Xiao et al. 2024](https://doi.org/10.3390/foods13142208). Title says monocular, while a snippet says a D435i captured the images [SNIP].
- **Citrus, RGB pose (Sun 2023) [SNIP]:** D435i, Nanning orchard, 79.79% harvest success, 11.13° mean rotation error — [Sun et al. 2023](https://doi.org/10.1016/j.compag.2023.108022).
- **Orchard scene metric depth, no fruit target (OrchardDepth) [SNIP]:** RMSE reduced from 1.5337 to 0.6738 against a baseline, unit not shown in the snippet — [review page](https://themoonlight.io/review/orcharddepth-precise-metric-depth-estimation-of-orchard-scene-from-monocular-camera-images).
- **Table grape peduncle (Coll-Ribes) [SNIP], other crop:** snippet gives "mean squared error of 2.66 cm" within 1 m, with an odd unit for MSE — [IRI-UPC](https://www.iri.upc.edu/download/scidoc/2764).

**Multi-view, SfM, NeRF, Gaussian splatting**
- **Multiple-camera particle filter for fruit position (Mehta 2017) [SNIP], citrus group, fruit in test not confirmed:** handles image noise and centroid errors. No error figure seen — [Mehta et al. 2017](https://doi.org/10.1016/j.compag.2017.08.007).
- **Two RGB-D views on an artificial orange (Beldek 2025) [FULL]:** see next question — [Beldek et al. 2025](https://arxiv.org/pdf/2502.12406).
- **3DGS for annotation, apple (van de Ven 2025) [SNIP], other fruit:** 3DGS reduces labelling (105 manual annotations produced 28,191 labels). Position estimates worsen with occlusion. No mm figure in what I saw. It supports training data, not direct localization — [van de Ven et al. 2025](https://arxiv.org/abs/2512.20148v1).
- **Orchard metric-semantic mapping, not citrus-specific (2024) [SNIP]:** mask-projected point-cloud centroid refined by minimizing reprojection error across frames — [arXiv 2409.19786](https://arxiv.org/pdf/2409.19786).

### Inferences
- Stereo depth error grows roughly with Z²/(f·b). This is standard geometry, and the numbers below use **my assumed parameters, not sourced ones**: with 0.25 px disparity error, a 120 mm baseline and f ≈ 1000 px give about 2 mm at 1 m and 4.7 mm at 1.5 m. A 50 mm baseline and f ≈ 600 px give about 8 mm at 1 m. This fits the observed pattern that wider-baseline stereo holds up better at range, and Font's growth of error with distance.
- For an orange project, the evidence-backed shortlist is ZED 2/2i (only citrus field-depth paper with a mm figure) and a ToF camera if working at 1.5–2 m in direct sun. The D435 family is reasonable at close range under canopy, on kiwifruit evidence that does not transfer directly.
- Learned monocular depth is not yet supported as a primary coordinate source for citrus: the sole citrus paper reports unitless error.

### Gaps
- No citrus result for ToF or LiDAR fusion with a mm error. A Chinese patent on spherical citrus point-cloud completion turned up, but no peer-reviewed evaluation [SNIP](https://vufind-test.katalog.k.utb.cz/SummonRecord/FETCH-epo_espacenet_CN117727028A3).
- No NeRF or Gaussian-splatting fruit coordinate error found for any fruit. No MiDaS or Depth Anything harvest-point error on citrus found. A snippet gave Depth Anything V2 RMSE 1.52 and MAE 1.28 for immature-green-fruit length, without units, and I could not tie it to a specific paper, so do not cite it.
- Intel's datasheet could not be opened (DNS failure), so D400 specifications are second-hand. Current D400 and Azure Kinect availability was not verified: the Microsoft page is archived, and a snippet of Neupane notes Intel announced discontinuing its RGB-D products in August 2021.

## How is the 3D point computed from a detection, and how do methods compare?

### Takeaway
Most pipelines back-project a box centre or mask region through depth, which returns a point on the visible surface. Adding the fruit radius or fusing views reduces the error for centre-grasping. The only paired citrus-like comparison (artificial orange, indoors) shows 24 → 14 → 4.4 mm from single-camera box centre to two-view analytic to learned two-view, and I found no paired mm comparison of sphere fitting against centroid on citrus.

### Cited Findings

**Method catalogue**
- **Box centre + depth + radius offset (oranges used for training):** YOLOv5 box centre; depth z_min at the centre pixel; z_f = z_min + the 3D distance corresponding to the horizontal semi-axis, assuming a circularly symmetric ellipsoid. Sensor is a RealSense D435. Perception was tested on real RGB-D images and control in simulation, and I saw no fruit coordinate error in that version [FULL] — [Gursoy et al. 2023](https://arxiv.org/abs/2306.08729). A later working paper with the same lead author, on Baxter and BAZAR, reports 3D localization MAE of 7.8–21.1 mm and lab harvest of 5 oranges and 6 apples. The abstract does not say which value applies to which case [ABS] — [Gursoy et al. 2025](https://esploro.umontpellier.fr/esploro/outputs/workingPaper/Two-Arms-One-Goal-Reproducible-Dual-Arm/99152943709311).
- **Box + colour segmentation + depth inpainting + imaging model (citrus):** Cr-Cb mapping, Otsu, morphology and convex hull define the fruit region. Kriging fills missing depth. The point Q0 is the 2D box centre back-projected through the depth map, which the authors state corresponds to the centre of the citrus *surface*. dz is regressed from dx and dy (137 fruits, RMSE 4.51 mm, R² 0.940) [FULL] — [Hou et al. 2022](https://doi.org/10.3389/fpls.2022.972445).
- **Results in Hou 2022 [FULL]:** distance error 3.98 mm; mean diameter errors dx 2.75, dy 2.52, dz 2.11 mm (22 images, caliper). Kriging restoration test, with about 50% of depth pixels artificially removed, gave errors of 2.29, 2.15, 2.08 and 2.31 mm across the four patterns. Text gives a mean of 2.21 mm and 1.36% relative error, while the paper's conclusion says 2.02 mm and 1.26%, an **internal inconsistency**. X and Y coordinate errors are not reported, and no error is split by illumination or occlusion.
- **Stem and picking-point via oriented point-cloud box (citrus):** YOLOv5s ROI + depth → point cloud → oriented bounding box for stem orientation → hand-eye transform. Average picking success 82%, described as a 50% improvement over no stem estimation. The abstract gives no mm error [ABS] — [Ye et al. 2025](https://doi.org/10.3390/agriculture15222330). A snippet attached 8.63 mm / 2.76% to this paper, but those match Hou 2024's values exactly, so it is probably a citation. Do not attribute it to Ye without the full text.
- **Point-cloud pose fitting (citrus):** YOLOv5s + RANSAC-LM fitting on a low-cost RGB-D camera. No numbers seen [SNIP] — [Zhang et al. 2024](https://doi.org/10.1016/j.eja.2024.127418).
- **Sphere RANSAC (apple, other fruit):** fruit idealized as a sphere and branch as a line. Reported metric is picking-direction angle: mean 11.81°, SD 13.65°, 0.543 s [ABS] — [Gao et al. 2022](https://doi.org/10.3390/agriculture12081170). A snippet of the same paper says sphere fitting improves localization and that using the surface point-cloud centroid as the fruit centre has large error, but gives no mm pairing [SNIP].
- **Mask → point cloud → filtered centre (apple, other fruit):** YOLACT-style mask, projection to LiDAR cloud, z-score outlier removal, centre of remaining points [FETCH] — [Kang et al. 2022](https://ar5iv.labs.arxiv.org/html/2205.00404).
- **Learned point network (apple, other fruit):** a PointNet grasp estimator is described as significantly better than RANSAC and Hough sphere fitting. Numbers were not extracted [SNIP] — [arXiv 2003.13298](https://arxiv.org/pdf/2003.13298).
- **Shape completion (strawberry, other fruit) [VIA Hou 2022]:** centre error 5.7 mm (Ge 2020), larger with overlapping fruit — [Hou et al. 2022](https://doi.org/10.3389/fpls.2022.972445).
- **Euclidean clustering (apple) [VIA Hou 2022]:** coordinates and diameter errors slightly below 10 mm (Nguyen 2016) — [Hou et al. 2022](https://doi.org/10.3389/fpls.2022.972445).
- **Stereo matching on detected boxes:** Faster R-CNN detection, window zooming for matching, triangulation with two colour CCD cameras [ABS, numbers not seen] — [Wang et al. 2019](https://doi.org/10.1109/access.2019.2925812). Font's centroid-only matching reduces matching cost, under 30 ms in a lab segmentation pipeline [FULL] — [Font et al. 2014](https://doi.org/10.3390/s140711557).

**Within-study comparisons (the only fair comparisons)**

Beldek 2025 [FULL]: artificial 35 mm-radius orange on artificial tree, indoors. Two RealSense D415 (one fixed, one eye-in-hand), YOLOv8-n, OptiTrack motion capture reference (mean ray error 0.754 mm), 48 fruit poses, 80/20 split. Error is to the **geometric centre**, the reference is independent, and the test set is about 10 poses — [Beldek et al. 2025](https://arxiv.org/pdf/2502.12406).

| Method | MAE x / y / z (mm) | Mean Euclidean (mm) | Picking success |
|---|---|---|---|
| Single eye-in-hand: box centre + radius offset | 19.24 / 8.05 / 11.92 | 24.02 | 77.7% |
| Two-camera analytic | 9.87 / 5.59 / 8.63 | 14.25 | 81.4% |
| Two-camera + AdaBoost regression | 3.71 / 2.13 / 1.07 | 4.40 | 88.8% |

The learned models assume one fixed 35 mm radius, which the authors say makes the data near-linear. Linear regression performs about the same as AdaBoost. The body text disagrees with its own table on some values (LR MED 4.15 in text, 4.46 in table; model labels also shift between text and table), so I took the AdaBoost and analytic rows from the abstract-confirmed figures.

Zhu 2026 [FULL], apple, other fruit: ToF at about 1 m, 124 paired occluded and unoccluded instances. **Reference is the unoccluded view's own 3D point at the box centre**, so these are consistency errors, not absolute accuracy, and they favour a centre-based estimator by construction — [Zhu et al. 2026](https://arxiv.org/pdf/2606.14089).

| Method | Unoccluded MAE / p95 (mm) | Occluded MAE / p95 (mm) | p50 latency (ms) |
|---|---|---|---|
| Centre-weighted depth (only with central support when occluded) | 1.054 / 2.960 | 6.876 / 28.246 | 0.130 |
| DBSCAN cluster centroid | 5.183 / 10.600 | 8.104 / 19.750 | 10.36 |
| Conditional combination | 1.054 / 2.960 | 8.882 / 27.596 | 0.142 |

The paper's example shows DBSCAN centroid depth of 816 mm against 803.5 mm for centre-weighted, a 12.5 mm inward shift it attributes to non-uniform surface sampling.

### Inferences
- **Define the target point first.** The right estimator depends on the gripper: a suction cup wants the visible surface, as in Zhu, while a parallel gripper or enclosing hand wants the geometric centre, as in Beldek. A paper's "3.98 mm" to the surface (Hou) says nothing about centre error, which also depends on radius and fruit shape.
- For oranges, a surface point plus a measured radius is a low-cost centre estimate. Hou's diameter errors of about 2–3 mm suggest radius adds roughly 1–1.5 mm, if the same diameter accuracy held on the target variety. Near-spherical fruit makes this cheaper than point-cloud completion, though no paper tests that comparison on citrus.
- Simple centroids and cluster centres are biased when visible coverage is partial. Sphere fitting should correct that in principle, but its benefit in mm on real citrus under occlusion is unmeasured.
- Beldek's regressor should not be assumed to generalize: it was trained on one rigid fruit size in fixed lighting.

### Gaps
- No paired test on real citrus of box-centre, mask-median, centroid, RANSAC sphere, least-squares sphere, completion and 3D detection against an independent reference. This is a clear experiment the project could run and publish.
- 3D detection networks and keypoints: no citrus coordinate error found. A pomegranate F-PointNet paper appeared but was not read [link, unread](https://www.sciencedirect.com/science/article/abs/pii/S0168169922005476).

## How is the camera-to-robot frame handled?

### Takeaway
Citrus vision papers often stop at the camera frame. Hand-eye error is commonly a few mm, comparable to depth error, and it is largely unreported in citrus error figures, so vision-only numbers understate the error at the gripper.

### Cited Findings
- **No robot frame at all:** Hou 2022 uses ZED factory intrinsics and reports errors in the camera frame only, with no hand-eye step or robot test [FULL] — [Hou et al. 2022](https://doi.org/10.3389/fpls.2022.972445).
- **Intrinsics:** Font estimates intrinsics and stereo extrinsics (calibration table reports focal lengths around 846–866 px and a 60.6 mm measured baseline). Calibration cut apple distance error at 2025 mm from 288.93 to 65.14 mm [FULL] — [Font et al. 2014](https://doi.org/10.3390/s140711557).
- **Eye-in-hand + fixed, on orange mock-up:** eye-in-hand transform via ViSP hand-eye calibration (200 iterations) plus Franka kinematic chain. Fixed camera extrinsics "extracted manually" (–60° rotation plus offsets). Intrinsics calibrated once on the argument that both cameras are the same model, which is a questionable assumption between individual units [FULL] — [Beldek et al. 2025](https://arxiv.org/pdf/2502.12406).
- **Hand-eye accuracy measured (peach, other fruit, indoor simulated) [FETCH]:** JAKA Zu 5 (±0.02 mm repeatability), TuYang TM460-E2 eye-in-hand, circular calibration board, Danish-weighted SVD. Mean absolute error 3.893 mm against 4.180 (SVD), 4.004 (LM) and 4.003 (Danish-DQ). Per-axis mean/max: X 1.365/4.022, Y 1.428/4.733, Z 2.675/7.454 mm. Z worsens with range: far mean 4.84/max 12.69 mm, close mean 2.87/max 7.62 mm. Six peaches: 3.57–4.83 mm, which authors call "basically within 5 mm" and sufficient — [Zhang et al. 2023 hand-eye](https://doi.org/10.3389/fpls.2022.1099033).
- **Eye-to-hand argument (apple) [FULL]:** frame-fixed ToF about 1 m from the workspace gives a stable view and avoids motion blur and depth degradation in eye-in-hand. The cost is arm occlusion, handled by a view-management strategy that re-captures when the arm has left the view. Position is mapped with a pre-calibrated rigid transform — [Zhu et al. 2026](https://arxiv.org/pdf/2606.14089).
- **Eye-in-hand with closed-loop approach [FULL]:** Font uses stereo for a rough approach to about 250 mm, then iterative image-based centring, which compensates lateral displacement at the cost of time (7.9 s fine approach of about 16 s total) — [Font et al. 2014](https://doi.org/10.3390/s140711557).
- **Citrus visual servo [SNIP]:** robust image-based visual servo tested with an artificial citrus fruit moving 120 mm, reported as stable closed-loop operation — [Mehta et al. 2016](https://portfolio.erau.edu/en/publications/robust-visual-servo-control-in-the-presence-of-fruit-motion-for-r/). DOI not confirmed; the listing gives *Comput. Electron. Agric.* 123:362–375.
- **Citrus dual-robot [ABS]:** iterative and closed-form dual-robot calibration, 82% picking success, no calibration error in the abstract — [Bao et al. 2024](https://doi.org/10.1049/tje2.12419).
- **Citrus hand-eye use [ABS]:** Ye 2025 uses hand-eye transform to drive the effector, with no accuracy figure — [Ye et al. 2025](https://doi.org/10.3390/agriculture15222330).
- **LiDAR-camera extrinsics (apple) [FETCH]:** target-based ASAC 2.03 px mean reprojection (0.78 px normalized); targetless Yuan et al. 1.91 px (0.66 px). Authors see similar accuracy and find targetless more convenient — [Kang et al. 2022](https://ar5iv.labs.arxiv.org/html/2205.00404).
- **Laser-camera calibration (apple system) [FULL]:** better model + RANSAC outlier rejection reduced mean depth calibration error from 4.91 to 0.39 mm — [Zhang et al. 2023](https://arxiv.org/abs/2311.02500).
- **General process and error propagation [FULL]:** review stresses that errors transmit through the calibration, image-processing and control chain, that random errors are hard to model, and that system-level vision-mechanism fault tolerance is required — [Tang et al. 2020](https://doi.org/10.3389/fpls.2020.00510).

### Inferences
- A rough budget for an uncorrelated stack, for illustration only: 4 mm depth (Hou, best case) with about 4 mm hand-eye (peach study) gives about 5.7 mm before kinematics, fruit motion or occlusion. Field values would be higher. Measure end-to-end at the gripper tool centre point, not only camera depth.
- Eye-in-hand allows a second, closer measurement, where stereo and ToF noise is smaller and depth Z error is reduced. Eye-to-hand gives a stable global view. Beldek's results suggest combining them improves accuracy, though on a mock-up. Fixed-plus-wrist is a sensible design to test.

### Gaps
- No citrus paper found reporting measured hand-eye error together with orchard fruit error.
- No study found of calibration drift from vibration, temperature or platform motion during citrus field work.

## How do sunlight, occlusion, distance and depth holes affect localization, and how is that mitigated?

### Takeaway
Sunlight is the main threat to IR active stereo and early ToF, occlusion is the main threat to centre estimates, and error grows with distance. Mitigations with evidence are ToF or LiDAR sensors, physical shading, close re-imaging, depth inpainting and rejecting poor targets, but numeric citrus results per condition barely exist.

### Cited Findings

**Sunlight**
- **Sensor choice:** see Neupane's specification and recommendation above [ABS] — [Neupane et al. 2021](https://doi.org/10.3390/agronomy11091780).
- **Kinect v2 outdoors [SNIP]:** fill rate near 0 in strong outdoor light on a phenotyping robot — [arXiv 2011.01022](https://arxiv.org/pdf/2011.01022).
- **D415 [SNIP], grape:** most accurate indoors, reduced performance outdoors — [Sensors 22(11):4179](https://mdpi.com/1424-8220/22/11/4179).
- **Conflicting review position [FULL]:** Tang 2020 calls ToF sensitive to interference, possibly failing in strong light, and recommends passive binocular for stability. It also groups "RGB-D" with ToF, which overlooks active-stereo cameras like the D400 — [Tang et al. 2020](https://doi.org/10.3389/fpls.2020.00510). Neupane's later measurements favour specific newer ToF cameras in sunlight.
- **Physical shading (apple) [FULL]:** retractable sun screen; authors credit elimination of earlier camera exposure failures, with 80.0% per-attempt success over 1,738 cycles and four sessions — [Zhu et al. 2026](https://arxiv.org/pdf/2606.14089). The system changed in other ways too, so shading is not isolated as a cause, and 80.0% is per attempt.
- **Over-the-row shade [VIA Tang 2020], apple:** Gongal 2016 tunnel structure — [Tang et al. 2020](https://doi.org/10.3389/fpls.2020.00510).
- **Thermal caution [FULL]:** Azure Kinect is rated only for 10–25 °C, so outdoor use may need active cooling — [Microsoft](https://learn.microsoft.com/en-us/previous-versions/azure/kinect-dk/hardware-specification).
- **Citrus detection under lighting [FULL]:** recall 99.55% non-uniform, 98.47% weak, 98.48% good lighting, but localization error is not split by condition. Overexposure produces incomplete fruit shapes and sparse depth under low light, as described qualitatively — [Hou et al. 2022](https://doi.org/10.3389/fpls.2022.972445).

**Occlusion**
- **Apple [FULL]:** MAE rises from 1.054 to 6.876–8.882 mm, with p95 from 2.96 to about 20–28 mm. Consistency metric, as noted above. Heavy leaf occlusion is a named cause of perception failure — [Zhu et al. 2026](https://arxiv.org/pdf/2606.14089).
- **Citrus on branch [SNIP]:** occlusion and adhesion lowered recognition success to 63.8% in a 2018 *Sensors* RealSense paper — [DOAJ record](https://doaj.org/article/6f2583f4506f47da8c1ceb763c79cdfd).
- **Citrus mitigation [FULL]:** convex hull of Otsu mask to recover occluded area, kriging to estimate depth inside it — [Hou et al. 2022](https://doi.org/10.3389/fpls.2022.972445).
- **Avoiding bad targets [FULL]:** Font proposes discarding occluded or asymmetric candidates, or blowing air to move leaves — [Font et al. 2014](https://doi.org/10.3390/s140711557). Tang notes laser beams can be blocked by obstacles [FULL] — [Tang et al. 2020](https://doi.org/10.3389/fpls.2020.00510).
- **Leaf manipulation (other crops) [SNIP, title only]:** active methods exist — [arXiv 2409.17389](https://arxiv.org/pdf/2409.17389).

**Distance**
- **Font 2014 apple [FULL]:** distance error is not monotonic at close range but rises to 65 mm at 2 m on a 60 mm baseline — [Font et al. 2014](https://doi.org/10.3390/s140711557).
- **D455 against LiDAR [FETCH]:** D455 SD rises from about 1.0 to 1.36 cm over 0.5–1.8 m, while LiDAR stays around 0.2–0.28 cm — [Kang et al. 2022](https://ar5iv.labs.arxiv.org/html/2205.00404).

**Depth holes**
- **ZED 2 on citrus [FULL]:** missing values can exceed half of the fruit area, attributed to camera limitations, lighting and angle. Kriging test error is about 2.1–2.3 mm, on an artificially masked map of **one shown example**, with worst cases where gaps fall on the most discontinuous part of the depth map — [Hou et al. 2022](https://doi.org/10.3389/fpls.2022.972445).
- **Fill rate as a metric [ABS]:** Neupane recommends reporting fill rate, bias-corrected RMSE and bias at 50 cm intervals to 3 m, under both artificial light and sunlight — [Neupane et al. 2021](https://doi.org/10.3390/agronomy11091780).

**Fruit motion**
- **Review [FULL]:** dynamic disturbance is called unsolved; a moving fruit's image shape differs from the initial capture, causing large 3D error — [Tang et al. 2020](https://doi.org/10.3389/fpls.2020.00510).

### Inferences
- Hou's kriging test removes valid pixels from a good map, so it measures interpolation on smooth surfaces and likely understates errors where a leaf truly replaces the fruit surface.
- Adopting Neupane's protocol would make this project's results comparable, and costs little.
- Occlusion mainly widens the tail, shown by p95 values far above MAE. Report p95 or success-within-tolerance, not the mean alone.

### Gaps
- No citrus study found reporting 3D localization error by sunlight level, occlusion level or distance bin.
- Effect of the waxy, specular citrus peel on ToF or active-stereo depth was not found.
- Comparison of direct against backlit canopy in orange orchards was not found.

## What is the reported error for citrus, compared with other spherical fruit and with end-effector tolerance?

### Takeaway
Credible citrus field fruit-position numbers come from very few studies, with best-case values of about 4–13 mm, and n is small. Those values are within the only explicit tolerance found (about 15 mm for an apple suction cup), but I found no citrus-specific mm tolerance, and citrus picking point error (about 9 mm) matters more if the stem must be cut.

### Cited Findings

**Citrus and orange**

| Study | Sensor / scene | Target and metric | Error | Reference and n | Tag |
|---|---|---|---|---|---|
| [Hou 2022](https://doi.org/10.3389/fpls.2022.972445) | ZED 2, orchard, 30–150 cm | Surface point, camera distance, mean error | 3.98 mm | Laser rangefinder, 22 images | FULL |
| [Lin 2019](https://doi.org/10.1016/j.biosystemseng.2019.06.019) | RGB-D, in-field, sensor model unconfirmed | x, y, z signed mean ± SD | 7.0 ± 2.5, −4.0 ± 3.0, 13.0 ± 3.0 mm | Not seen; 506-image dataset, F1 0.9197 | SNIP |
| [Hou 2024](https://doi.org/10.1007/s11119-024-10169-2) | Binocular | Picking point MAE | 8.63 mm (MRE 2.76%) | Not seen | SNIP |
| [Mehta & Burks 2014](https://doi.org/10.1016/j.compag.2014.01.003) | Moving monocular | Controller overall | About 15 mm | Not seen | VIA Kang |
| [Gursoy 2025](https://esploro.umontpellier.fr/esploro/outputs/workingPaper/Two-Arms-One-Goal-Reproducible-Dual-Arm/99152943709311) | RGB-D, lab, oranges and apples | 3D MAE | 7.8–21.1 mm | Not seen | ABS |
| [Beldek 2025](https://arxiv.org/pdf/2502.12406) | 2× D415, indoor, **artificial** orange | Geometric centre, Euclidean | 24.02 / 14.25 / 4.40 mm | Motion capture, 48 poses | FULL |
| [Chinese lab study 2023](https://www.aeeisp.com/zgnjhxb/article/doi/10.13733/j.jcam.issn.2095-5553.2023.09.021) | RealSense R200, lab, random fruit layout | Mean position | 1.22 cm; 80% picking | Not seen; authors not captured | SNIP |
| [Kong 2023](https://doi.org/10.3390/agronomy13082122) | Monocular, 30–60 cm | Depth MAE, RMSE | 0.53, 0.53, **no units** | Not seen | ABS |
| [Yang 2020](https://doi.org/10.1016/j.compag.2020.105469) | Mask R-CNN + depth | Diameter only | <4 mm; distance not provided | Not seen | VIA Hou 2022 |

**Pose and success without mm position:** Xiao 2024 *Foods* 7.9°, 85.1% field picking [ABS]; [Xiao 2024 *Agriculture*](https://doi.org/10.3390/agriculture14081227) 87.15% arm, 82.4% field picking [ABS]; Sun 2023 11.13°, 79.79% [SNIP]; Ye 2025 82% [ABS]; Bao 2024 82% [ABS].

**Other fruit, labelled** (mostly listed above)
- **Apple:** ALACS 6.9–11.2 mm against RealSense 21.5 mm indoors, 1.0–1.6 m [ABS]; Si 2015 <20 mm [VIA]; Font 2014 21 mm at about 1 m on a low-cost webcam, lab [FULL]; Nguyen 2016 about 10 mm [VIA]; Zhu 2026 1–9 mm (self-reference) [FULL].
- **Tomato:** winter jujube and bunch-tomato stem snippets exist, with X/Y/Z under 5 mm (jujube) and depth within ±2.5 mm at the picking point (tomato stem) [SNIP] — [Plant Phenomics 0258](https://spj.science.org/doi/10.34133/plantphenomics.0258), [PMC11637874](https://pmc.ncbi.nlm.nih.gov/articles/PMC11637874).
- **Peach:** 3.57–4.83 mm indoors, simulated, on a ToF camera, including hand-eye [FETCH] — [Zhang 2023](https://doi.org/10.3389/fpls.2022.1099033).
- **Strawberry:** 5.7 mm [VIA]. **Litchi:** 15 mm [VIA Hou 2022]. **Mango:** 4.9 mm (dimension error) [VIA Hou 2022].

**End-effector tolerance**
- **Apple suction cup [FULL]:** attaches with up to 1.5 cm offset from fruit centre in lab tests, which the authors consider enough for outdoor ToF — [Zhu et al. 2026](https://arxiv.org/pdf/2606.14089). An earlier paper from the same group also gives about 1.5 cm attraction range — [Zhang et al. 2023](https://arxiv.org/abs/2311.02500).
- **Soft strawberry gripper [SNIP]:** 10 mm maximum per axis — [arXiv 2601.02085](https://arxiv.org/pdf/2601.02085).
- **Tomato roller gripper [SNIP]:** tolerated a 9 mm one-side offset (1.33% failure) and 6 mm per side (4%) — [Agriculture 15(2):220, attribution unconfirmed](https://www.mdpi.com/2077-0472/15/2/220).
- **Peach study [FETCH]:** authors treat 5 mm as sufficient, without a gripper test reported in what I saw — [Zhang 2023](https://doi.org/10.3389/fpls.2022.1099033).
- **Depth camera specification [ABS]:** 20 mm bias-corrected RMSE at 2 m for fruit localization and sizing — [Neupane et al. 2021](https://doi.org/10.3390/agronomy11091780).
- **Citrus [ABS]:** Xiao 2024 designs a flexible hand so adaptability "makes up" for localization inaccuracy, and names out-of-range fruit and joint motion errors as the main positioning failure causes — [Xiao et al. 2024](https://doi.org/10.3390/agriculture14081227). Field failures here are not vision-only.

**Does accuracy change outcomes?**
- **Orange mock-up [FULL]:** success climbs 77.7 → 81.4 → 88.8% as error falls 24.02 → 14.25 → 4.40 mm — [Beldek et al. 2025](https://arxiv.org/pdf/2502.12406).
- **Apple [ABS]:** 95% against 71% detachment for laser scanning against RealSense — [Chu et al. 2023](https://arxiv.org/abs/2311.08674).
- **Citrus stems [ABS]:** adding stem pose improves success by a reported 50% — [Ye et al. 2025](https://doi.org/10.3390/agriculture15222330).
- **Review baseline [FULL, citing Arad 2020]:** prototypes average about 66% success (40–86%) and 33 s per fruit (1–227 s) — [Tang et al. 2020](https://doi.org/10.3389/fpls.2020.00510).

### Inferences
- In an orchard, Hou's 3.98 mm is a best-case, axial, surface measure on a few near-centre fruit. Lin's 13 mm depth bias is a more cautious planning figure, if confirmed. As my own judgement, not a sourced figure, plan for 10–25 mm of error at the gripper until end-to-end tests say otherwise.
- With a hand wide enough to envelop an orange (I assumed 70–80 mm diameter, unsourced except Beldek's 70 mm mock-up), centre errors of 10–15 mm are likely tolerable (my judgement from the apple suction and tomato figures, not measured on citrus). Stem-cutting tools will need much tighter values, because the target is a thin stem, and 8.63 mm may not be good enough.
- Field success is limited by more than coordinates. Reach, branches, seal or grasp failures and joint errors also appear in the failure reports.

### Gaps
- No citrus-specific mm tolerance found. It would have to be measured for the project's end effector, as an offset-against-success curve.
- Lin 2019 and Hou 2024 full texts could not be opened, so reference method, range and sensor are unconfirmed. Get them before citing these numbers.
- No 2026 citrus-specific localization paper with mm errors surfaced; recent coverage may be incomplete since my search tools index publisher pages unevenly.
- No independent replication found of any citrus figure. Hou 2022 shares data and code ([GitHub](https://github.com/AshesBen/citrus-detection-localization)), so it could be re-tested, though I did not check the repository.
- Snippets also gave SOLOv2 apple axis errors (0–3.95, 0–5.16, 0–1 mm, 60 samples) and green-apple sizing RMSE of 2.35 mm (Azure Kinect) against 9.65 mm (D435i). I could not tie these to specific papers with confidence, so they are excluded from the findings.

### Full citations
- Bao X., Shi X., Ma X., Leng J., Ma Z., Ren M., Li S. (2024). Design and experiment of citrus picking system based on dual robot collaboration. *The Journal of Engineering*. https://doi.org/10.1049/tje2.12419
- Beldek C., Dunn A., Cunningham J., Sariyildiz E., Phung S. L., Alici G. (2025). Multi-vision-based Picking Point Localisation of Target Fruit for Harvesting Robots. arXiv:2502.12406. https://arxiv.org/abs/2502.12406
- Chu P., Li Z., Zhang K., Lammers K., Lu R. (2023). High-Precision Fruit Localization Using Active Laser-Camera Scanning: Robust Laser Line Extraction for 2D-3D Transformation. arXiv:2311.08674. https://arxiv.org/abs/2311.08674
- Font D., Pallejà T., Tresanchez M., Runcan D., Moreno J., Martínez D., Teixidó M., Palacín J. (2014). A Proposal for Automatic Fruit Harvesting by Combining a Low Cost Stereovision Camera and a Robotic Arm. *Sensors* 14:11557–11579. https://doi.org/10.3390/s140711557
- Gao R., Zhou Q., Cao S., Jiang Q. F. (2022). An Algorithm for Calculating Apple Picking Direction Based on 3D Vision. *Agriculture* 12(8):1170. https://doi.org/10.3390/agriculture12081170
- Gursoy E., Navarro B., Cosgun A., Kulić D., Cherubini A. (2023). Towards vision-based dual arm robotic fruit harvesting. arXiv:2306.08729; a record lists acceptance at IEEE CASE 2023. https://arxiv.org/abs/2306.08729
- Gursoy E., Cosgun A., Kulić D., Cherubini A. (2025). Two Arms, One Goal: Reproducible Dual-Arm Robotic Fruit Harvesting. Working paper, HAL / Université de Montpellier. https://esploro.umontpellier.fr/esploro/outputs/workingPaper/Two-Arms-One-Goal-Reproducible-Dual-Arm/99152943709311
- Hou C., Zhang X., Tang Y., Zhuang J., Tan Z., Huang H., Chen W., Wei S., He Y., Luo S. (2022). Detection and localization of citrus fruit based on improved You Only Look Once v5s and binocular vision in the orchard. *Frontiers in Plant Science* 13:972445. https://doi.org/10.3389/fpls.2022.972445
- Hou C., Xu J., Tang Y., Zhuang J., Tan Z., Chen W., Wei S., Huang H., Fang M. (2024). Detection and localization of citrus picking points based on binocular vision. *Precision Agriculture* 25:2321–2355. https://doi.org/10.1007/s11119-024-10169-2
- Kang H., Wang X., Chen C. (2022). Accurate Fruit Localisation for Robotic Harvesting using High Resolution LiDAR-Camera Fusion. arXiv:2205.00404; arXiv page links DOI 10.1016/j.compag.2022.107450 as related. https://arxiv.org/abs/2205.00404
- Kong D., Wang J., Zhang Q., Li J., Rong J. (2023). Research on Fruit Spatial Coordinate Positioning by Combining Improved YOLOv8s and Adaptive Multi-Resolution Model. *Agronomy* 13(8):2122. https://doi.org/10.3390/agronomy13082122
- Lin G., Tang Y., Zou X., Li J., Xiong J. (2019). In-field citrus detection and localisation based on RGB-D image analysis. *Biosystems Engineering* 186:34–44. https://doi.org/10.1016/j.biosystemseng.2019.06.019
- Liu X., Jing X., Jiang H., Younas S., Wei R., Dang H., Wu Z., Fu L. (2024). Performance evaluation of newly released cameras for fruit detection and localization in complex kiwifruit orchard environments. *Journal of Field Robotics*. https://doi.org/10.1002/rob.22297
- Mehta S. S., Burks T. (2014). Vision-based control of robotic manipulator for citrus harvesting. *Computers and Electronics in Agriculture*. https://doi.org/10.1016/j.compag.2014.01.003
- Mehta S. S., MacKunis W., Burks T. F. (2016). Robust visual servo control in the presence of fruit motion for robotic citrus harvesting. *Computers and Electronics in Agriculture* 123:362–375. Publication page: https://portfolio.erau.edu/en/publications/robust-visual-servo-control-in-the-presence-of-fruit-motion-for-r/
- Mehta S. S., Ton C. T., Asundi S. A., Burks T. (2017). Multiple camera fruit localization using a particle filter. *Computers and Electronics in Agriculture*. https://doi.org/10.1016/j.compag.2017.08.007
- Neupane C., Koirala A., Wang Z., Walsh K. B. (2021). Evaluation of Depth Cameras for Use in Fruit Localization and Sizing: Finding a Successor to Kinect v2. *Agronomy* 11(9):1780. https://doi.org/10.3390/agronomy11091780
- Rustler L., Volprecht V., Hoffmann M. (2025). Empirical Comparison of Four Stereoscopic Depth Sensing Cameras for Robotics Applications. *IEEE Access* 13:67564–67577. https://arxiv.org/abs/2501.07421
- Sun Q., Zhong M., Chai X., Zeng Z., Yin H., Zhou G., Sun T. (2023). Citrus pose estimation from an RGB image for automated harvesting. *Computers and Electronics in Agriculture*. https://doi.org/10.1016/j.compag.2023.108022
- Tang Y., Chen M., Wang C., Luo L., Li J., Lian G., Zou X. (2020). Recognition and Localization Methods for Vision-Based Fruit Picking Robots: A Review. *Frontiers in Plant Science* 11:510. https://doi.org/10.3389/fpls.2020.00510
- van de Ven R. et al. (2025). Enhancing annotations for 5D apple pose estimation through 3D Gaussian Splatting (3DGS). arXiv:2512.20148. https://arxiv.org/abs/2512.20148v1
- Wang C., Luo T., Zhao L., Tang Y., Zou X. (2019). Window Zooming-Based Localization Algorithm of Fruit and Vegetable for Harvesting Robot. *IEEE Access*. https://doi.org/10.1109/access.2019.2925812
- Xiao X., Wang Y., Jiang Y., Wu H., Zhou B. (2024). Monocular Pose Estimation Method for Automatic Citrus Harvesting Using Semantic Segmentation and Rotating Target Detection. *Foods* 13(14):2208. https://doi.org/10.3390/foods13142208
- Xiao X., Wang Y., Zhou B., Jiang Y. (2024). Flexible Hand Claw Picking Method for Citrus-Picking Robot Based on Target Fruit Recognition. *Agriculture* 14(8):1227. https://doi.org/10.3390/agriculture14081227
- Yang C., Xiong L. Y., Wang Z., Wang Y., Shi G., Kuremot T., Zhao W., Yang Y. (2020). Integrated detection of citrus fruits and branches using a convolutional neural network. *Computers and Electronics in Agriculture*. https://doi.org/10.1016/j.compag.2020.105469
- Ye L., Ma J., Lv Y., Guo Z., Lai Z., Ou C., Li J., Wu F. (2025). The YOLO-OBB-Based Approach for Citrus Fruit Stem Pose Estimation and Robot Picking. *Agriculture* 15(22):2330. https://doi.org/10.3390/agriculture15222330
- Zhang G., Li L., Zhang Y., Liang J., Chun C.-P. (2024). Citrus pose estimation under complex orchard environment for robotic harvesting. *European Journal of Agronomy*. https://doi.org/10.1016/j.eja.2024.127418
- Zhang K., Chu P., Lammers K., Li Z., Lu R. (2023). Active Laser-Camera Scanning for High-Precision Fruit Localization in Robotic Harvesting: System Design and Calibration. arXiv:2311.02500. https://arxiv.org/abs/2311.02500
- Zhang X., Yao M., Cheng Q., Liang G., Feng F. (2023). A novel hand-eye calibration method of picking robot based on TOF camera. *Frontiers in Plant Science*. https://doi.org/10.3389/fpls.2022.1099033
- Zhu K., Lammers K., Arunachalam C., Zhang K., Lu R., Li Z. (2026, date inferred from arXiv ID). A Modular Dual-Arm Apple Harvesting Robot with Enhanced Field Performance. arXiv:2606.14089. https://arxiv.org/abs/2606.14089
