# Topological Characterization of Teeth on Panoramic Radiographs (Persistent Homology)

치아 영상의 형태를 **지속 호몰로지(persistent homology)**로 정량화해, 위상적 특징만으로
진단 클래스(우식/깊은우식/치근단병변/매복치)를 얼마나 구별할 수 있는지 보는 예비 연구.

> ⚠️ Preliminary study / technical report. Not peer-reviewed, not clinically validated.
> Data: DENTEX (MICCAI 2023), CC BY-NC-SA. 자소서 서사("위상수학으로 치아 형태를 읽는다")의 실물 근거.

## 왜 이 연구인가 (한 줄)
종이 위 매듭을 다루던 위상수학을 **실제 치아 영상의 구조**에 적용 — 형태의 위상적 지문(topological fingerprint)이 진단 신호를 담는지 검증.

## 방법
1. DENTEX 치아 크롭(프로젝트1과 공유) → 그레이스케일.
2. **큐빅 복합체(cubical complex)**로 이미지의 지속 호몰로지 계산(H0=연결성, H1=구멍/루프).
3. 위상 특징 추출: 지속시간 통계, **persistence entropy**, **Betti 곡선**, **persistence image**.
4. 위상 특징만으로 RandomForest 분류 → 클래스별 recall/혼동행렬. (형태만으로 어디까지 구별되나)
5. 클래스별 대표 **persistence diagram**·Betti 곡선 시각화.

## 구조
```
07_tooth_topology_project/
├── README.md · requirements.txt · config.yaml · RUN_GUIDE.md
├── src/
│   ├── topo_features.py   # cubical complex → 지속 호몰로지 → 특징 벡터
│   └── analyze.py         # 크롭 로드 → 특징 → 분류·그림
└── technical_note/technical_note.md
```

## 빠른 시작
```bash
pip install -r requirements.txt
# 프로젝트1의 data/crops 를 재사용 (config.yaml crops_dir로 지정)
python -m src.analyze --config config.yaml
# 결과: results/ (metrics.json, fig_betti.png, fig_pd_examples.png, fig_confusion.png)
```

## 정직성
- 결과 숫자는 본인 실행값(조작 0). 위상만으로 완벽 분류 주장 아님 — "형태가 신호를 담는다"의 예비 근거.
- DENTEX 라이선스·인용 준수.
