"""
치아 크롭 -> 지속 호몰로지 특징 -> RandomForest 분류 + 시각화.
위상 특징만으로 진단 클래스를 어디까지 구별하는지(형태가 신호를 담는가) 예비 검증.

    python -m src.analyze --config config.yaml
결과: results/metrics.json, fig_confusion.png, fig_betti_by_class.png,
      fig_pd_examples.png, fig_entropy_by_class.png
"""
import argparse, json, glob, os
from pathlib import Path

import numpy as np
import yaml
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score, f1_score, confusion_matrix, classification_report
from tqdm import tqdm

from .topo_features import topo_feature_vector, _persistence, _betti_curve


def load_config(p="config.yaml"):
    return yaml.safe_load(open(p))


def load_records(crops_dir):
    # 크롭 폴더(class 하위폴더)를 직접 glob → cwd·상대경로 문제 회피
    recs = []
    for cdir in sorted(glob.glob(str(Path(crops_dir) / "*"))):
        if os.path.isdir(cdir):
            lab = Path(cdir).name.replace("_", " ")
            for f in glob.glob(os.path.join(cdir, "*.png")):
                recs.append([f, lab])
    assert recs, f"no crops in {crops_dir} (프로젝트1 build-crops 먼저 실행)"
    return recs


def to_gray(path, size):
    img = Image.open(path).convert("L").resize((size, size))
    a = np.asarray(img, dtype=np.float32) / 255.0
    return a


def main(cfg):
    crops_dir = cfg["data"]["crops_dir"]; size = cfg["data"]["img_size"]
    tb = cfg["topo"]["betti_bins"]; pim = cfg["topo"]["pim_pixels"]; md = cfg["topo"]["max_dim"]
    out = Path(cfg["out_dir"]); out.mkdir(exist_ok=True)

    recs = load_records(crops_dir)
    classes = sorted({l for _, l in recs})
    cls2idx = {c: i for i, c in enumerate(classes)}
    X, y, keep = [], [], []
    _errs = []
    example_pd = {c: None for c in classes}
    betti_acc = {c: [] for c in classes}
    for path, lab in tqdm(recs, desc="topo features"):
        try:
            g = to_gray(path, size)
            fv, dgms = topo_feature_vector(g, tb, pim, md)
        except Exception as e:
            if len(_errs) < 3:
                _errs.append(repr(e))
            continue
        X.append(fv); y.append(cls2idx[lab]); keep.append((path, lab))
        if example_pd[lab] is None:
            example_pd[lab] = dgms
        pd1 = dgms.get(1, np.zeros((0, 2)))
        betti_acc[lab].append(_betti_curve(pd1, 0.0, 1.0, tb))
    if len(X) == 0:
        raise RuntimeError(f"모든 크롭에서 특징 추출 실패. 첫 에러: {_errs}")
    X = np.array(X); y = np.array(y)
    print(f"[topo] {len(X)} crops, dim={X.shape[1]}, classes={classes}")

    # 분류
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=cfg["clf"]["test_ratio"],
                                          random_state=cfg["clf"]["seed"], stratify=y)
    clf = RandomForestClassifier(n_estimators=cfg["clf"]["n_estimators"],
                                 class_weight="balanced", random_state=cfg["clf"]["seed"])
    clf.fit(Xtr, ytr); pred = clf.predict(Xte)
    rec = recall_score(yte, pred, average=None, labels=range(len(classes)), zero_division=0)
    metrics = {"n": int(len(X)), "dim": int(X.shape[1]), "classes": classes,
               "macro_f1": float(f1_score(yte, pred, average="macro", zero_division=0)),
               "recall_per_class": {classes[i]: float(rec[i]) for i in range(len(classes))},
               "report": classification_report(yte, pred, target_names=classes, zero_division=0)}
    json.dump(metrics, open(out / "metrics.json", "w"), ensure_ascii=False, indent=2)
    print(json.dumps({k: metrics[k] for k in ["macro_f1", "recall_per_class"]}, ensure_ascii=False, indent=2))

    # 혼동행렬
    cm = confusion_matrix(yte, pred, labels=range(len(classes)))
    plt.figure(figsize=(5, 4)); plt.imshow(cm, cmap="Blues")
    plt.xticks(range(len(classes)), classes, rotation=45, ha="right")
    plt.yticks(range(len(classes)), classes); plt.colorbar()
    plt.title("Topology-only classification"); plt.tight_layout()
    plt.savefig(out / "fig_confusion.png", dpi=150); plt.close()

    # 클래스별 평균 Betti(H1) 곡선
    plt.figure(figsize=(6, 4))
    for c in classes:
        if betti_acc[c]:
            plt.plot(np.mean(betti_acc[c], axis=0), label=c)
    plt.xlabel("filtration bin"); plt.ylabel("mean Betti-1"); plt.legend()
    plt.title("Mean H1 Betti curve by diagnosis"); plt.tight_layout()
    plt.savefig(out / "fig_betti_by_class.png", dpi=150); plt.close()

    # 클래스별 대표 persistence diagram (H0·H1)
    n = len(classes)
    plt.figure(figsize=(3 * n, 3))
    for i, c in enumerate(classes):
        ax = plt.subplot(1, n, i + 1)
        dg = example_pd[c] or {}
        for dim, col in [(0, "tab:blue"), (1, "tab:red")]:
            pdd = dg.get(dim, np.zeros((0, 2)))
            if len(pdd):
                ax.scatter(pdd[:, 0], pdd[:, 1], s=8, c=col, label=f"H{dim}")
        ax.plot([0, 1], [0, 1], "k--", lw=0.5)
        ax.set_title(c, fontsize=8); ax.set_xlabel("birth"); ax.set_ylabel("death")
    plt.tight_layout(); plt.savefig(out / "fig_pd_examples.png", dpi=150); plt.close()
    print(f"[saved] figures -> {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config.yaml")
    args = ap.parse_args()
    main(load_config(args.config))
