# Topological Fingerprints of Teeth on Panoramic Radiographs: A Persistent-Homology Preliminary Study

**Author:** Seunghyun Lee — ORCID [0009-0006-1926-653X](https://orcid.org/0009-0006-1926-653X)
**Date:** 2026-0X  **Type:** Preliminary technical report (not peer-reviewed)

> ⚠️ [FILL]은 본인 실행값으로 채운다(조작 금지). 블라인드 자소서 본문엔 실명·ORCID 미기재; 이 공개본에만.

## Abstract
치아 형태가 진단 신호를 담는지를 위상적으로 검증한다. DENTEX 파노라마의 치아 크롭 3,529개에 큐빅 복합체 기반 지속 호몰로지를 적용해 470차원 위상 특징(persistence entropy·Betti 곡선·persistence image)을 추출하고, **위상 특징만으로** 4개 진단 클래스를 분류했다(RandomForest, class_weight=balanced). macro-F1 0.30, 클래스별 recall은 Caries 0.96 / Impacted 0.26 / Deep Caries 0.04 / Periapical Lesion 0.00이었다. 즉 위상 특징은 흔하거나 구조적으로 뚜렷한 클래스에 치우치고 **미세 병소(우식·치근단)는 거의 구별하지 못했다.** 형태 정보만으로는 부족하며, 이는 픽셀·CNN 기반(프로젝트1의 XAI)과의 융합 필요성을 시사한다.

## 1. Introduction
- 배경: 위상수학(매듭·지속 호몰로지)으로 형태의 불변량을 다뤄 온 관점을 실제 치아 영상에 적용.
- 질문: 픽셀 밝기·CNN 특징 없이 **순수 위상 특징만**으로 진단 클래스가 구별되는가?

## 2. Data & Method
- DENTEX(MICCAI 2023) 치아 크롭(비상업 연구용). 클래스: Caries/Deep Caries/Periapical/Impacted.
- 그레이스케일 [FILL]px → 큐빅 복합체 sublevel 지속 호몰로지(H0,H1).
- 특징: 지속시간 통계·persistence entropy·Betti 곡선·persistence image → RandomForest(class_weight=balanced).

## 3. Preliminary Results (n=3,529, 470-dim, test 25%)
- 클래스별 recall(위상 특징만): **Caries 0.96 / Impacted 0.26 / Deep Caries 0.04 / Periapical Lesion 0.00**, macro-F1 **0.30**. (그림1: 혼동행렬 fig_confusion.png)
- 그림2: 클래스별 평균 H1 Betti 곡선 — 매복치가 다른 형태를 보임(fig_betti_by_class.png).
- 그림3: 대표 persistence diagram(클래스별, fig_pd_examples.png).
- 관찰: 위상 특징은 **구조적으로 뚜렷한 매복치**를 어느 정도 구별하나, **미세한 우식·치근단병변은 거의 구별하지 못함**(다수 클래스 Caries로 쏠림). 형태만으로는 드문 병소 신호가 부족.
- ⚠️ 클래스 불균형(Caries 2189 vs Periapical 158) 영향. 향후 균형 샘플링·CNN 특징 결합으로 개선 여지.

## 4. Limitations
2D 파노라마(3D 아님)·단일 데이터·예비·비임상. 위상 단독은 보조 특징이며 CNN 대체 아님.

## 5. Conclusion
치아 형태의 위상적 지문이 진단 신호를 부분적으로 담음을 예비적으로 확인. 향후 3D(CBCT)·CNN+TDA 융합으로 확장.

## Artifacts
Code: [GitHub URL] · This note: [Zenodo DOI] · Author ORCID: 0009-0006-1926-653X

## References
[1] DENTEX (MICCAI 2023). [정식 인용 FILL]
[2] Edelsbrunner & Harer, Computational Topology.
[3] GUDHI library.
