# 실행 → 공개 → 증빙 (프로젝트2: 치아 위상수학)

> 프로젝트1(06)의 `data/crops`를 재사용하므로, **06의 build-crops를 먼저 실행**해야 함.

## 실행
```bash
cd 07_tooth_topology_project
pip install -r requirements.txt        # gudhi, persim 포함
python -m src.analyze --config config.yaml
# results/: metrics.json, fig_confusion.png, fig_betti_by_class.png, fig_pd_examples.png
```
- 위상 특징만으로의 분류 성능이 목표 — 완벽할 필요 없음. "형태가 신호를 담는다"의 예비 근거면 충분.
- `config.yaml`의 `crops_dir`가 06의 크롭을 가리키는지 확인.

## 공개 = 증빙 (프로젝트1과 동일 절차)
1. **GitHub** 별도 레포로 push (예: `tooth-topology-persistent-homology`)
2. `technical_note.md` 실수치 채움 → **Zenodo DOI**(ZENODO_SETUP.md 절차, ORCID 저자 연결)
3. (선택) **Papers with Code**에 등록(코드+성능), **arXiv**(endorsement 시)

## 증빙·자소서 반영
- 실적표 새 행: "치아 파노라마 영상의 위상적 지문 예비연구 — 지속 호몰로지로 형태 정량화·진단 신호 검증(GitHub·Zenodo DOI, 단독)".
- 자소서 4번(연구)·12번(진로): "실제 치아 영상에 위상수학(지속 호몰로지)을 적용해 형태를 정량화해 보았다"(예비, 과장 금지).

## 정직성
- 결과 조작 0, 실패/한계 명시, 위상 단독은 보조라고 명확히. DENTEX 라이선스·인용.
