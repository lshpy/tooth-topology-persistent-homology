"""
치아 크롭(그레이스케일) -> 지속 호몰로지(cubical complex) -> 위상 특징 벡터.

특징: H0/H1 각각의 (개수, 지속시간 합/평균/최대), persistence entropy,
      Betti 곡선(샘플), + 전역 persistence image(H1).
"""
import numpy as np

try:
    import gudhi
except Exception:  # gudhi 미설치 시 명확한 안내
    gudhi = None

try:
    from persim import PersistenceImager
except Exception:
    PersistenceImager = None


def _persistence(img2d):
    """img2d: (H,W) float. sublevel cubical persistence. returns dict dim->Nx2 (birth,death)."""
    assert gudhi is not None, "pip install gudhi"
    cc = gudhi.CubicalComplex(top_dimensional_cells=img2d.astype(np.float64))
    cc.compute_persistence()
    out = {0: [], 1: []}
    fin = float(np.nanmax(img2d)) + 1.0
    for dim, (b, d) in cc.persistence():
        if dim not in out:
            continue
        d = fin if (d == float("inf")) else d
        out[dim].append([b, d])
    return {k: (np.array(v) if v else np.zeros((0, 2))) for k, v in out.items()}


def _pers_entropy(pairs):
    if len(pairs) == 0:
        return 0.0
    p = pairs[:, 1] - pairs[:, 0]
    p = p[p > 0]
    if p.sum() == 0:
        return 0.0
    q = p / p.sum()
    return float(-(q * np.log(q + 1e-12)).sum())


def _betti_curve(pairs, tmin, tmax, bins):
    xs = np.linspace(tmin, tmax, bins)
    if len(pairs) == 0:
        return np.zeros(bins)
    b = np.array([np.sum((pairs[:, 0] <= t) & (pairs[:, 1] > t)) for t in xs], dtype=float)
    return b


def topo_feature_vector(img2d, betti_bins=30, pim_pixels=20, max_dim=1):
    """img2d: (H,W) in [0,1]. -> 1D feature vector."""
    dgms = _persistence(img2d)
    tmin, tmax = float(np.nanmin(img2d)), float(np.nanmax(img2d)) + 1.0
    feats = []
    for dim in range(max_dim + 1):
        pd = dgms.get(dim, np.zeros((0, 2)))
        pers = (pd[:, 1] - pd[:, 0]) if len(pd) else np.array([])
        feats += [len(pd),
                  float(pers.sum()) if len(pers) else 0.0,
                  float(pers.mean()) if len(pers) else 0.0,
                  float(pers.max()) if len(pers) else 0.0,
                  _pers_entropy(pd)]
        feats += list(_betti_curve(pd, tmin, tmax, betti_bins))
    # persistence image for H1 (전역 형태 요약) — 고정 길이(N) 보장
    N = pim_pixels * pim_pixels
    vec = np.zeros(N, dtype=np.float32)
    if PersistenceImager is not None:
        pd1 = dgms.get(1, np.zeros((0, 2)))
        try:
            if len(pd1):
                pim = PersistenceImager(pixel_size=max(1e-3, (tmax - tmin) / pim_pixels))
                arr = np.asarray(pim.transform([pd1])[0]).flatten().astype(np.float32)
                vec[: min(N, arr.size)] = arr[:N]
        except Exception:
            pass
    feats += list(vec)
    return np.array(feats, dtype=np.float32), dgms
