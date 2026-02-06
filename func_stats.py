#!/usr/bin/env python3

## Significance testing functions
## Petra Sieber, Dec 2025

from scipy import stats
import numpy as np
import xarray as xr
import statsmodels as sm
from statsmodels.stats.multitest import multipletests
import itertools

# Significance testing on gridded data (xarray)
# Student t-test: parametric test for independent/dependent samples, data is normally distributed 
def ttest_2samp(da1, da2, paired=False, dim="time", global_alpha=0.05):
    """xarray wrapper for two-sample student's t test
    Paramters
    ---------
    da1, da2 : xr.DataArray
        arrays of samples
    paired : bool, default: False
        T-test unpaired or paired (identical to 1samp of difference, for correlated samples)
    dim : str, default: "time"
        Dimension along which to compute the test
    global_alpha, float, default: 0.05
        Global alpha of Benjamini and Hochberg correction, 2x the level for non-field significance tests in Wilks (2016)
        For two-tailed tests the non-field significance level has to be halved, which cancels the global significance multiplier
    
    """
    dim = [dim] if isinstance(dim, str) else dim

    def _ttest(x, y):
        if paired: # if True
            return stats.ttest_rel(x, y, axis=-1, nan_policy="omit").pvalue # paired (related samples); default is two-tailed
        else:
            return stats.ttest_ind(x, y, axis=-1, nan_policy="omit").pvalue # unpaired; default is two-tailed

    # use xr.apply_ufunc to handle vectorization
    result = xr.apply_ufunc(
        _ttest,
        da1,
        da2,
        input_core_dims=[dim, dim],
        output_core_dims=[[]],
        exclude_dims=set(dim),
        dask="parallelized",
        output_dtypes=[float],
    ).compute()

    # apply Benjamini and Hochberg correction
    shape = result.shape
    
    values = result.values.ravel()
    notnull = np.isfinite(values)

    p_adjust = multipletests(
        values[notnull], alpha=global_alpha, method="fdr_bh"
    )[0]
    values[notnull] = p_adjust
    result.values = values.reshape(shape)

    return result

# Mann-Whitney U rank test: non-parametric test for independent samples
# Wilcoxon rank-sum test: non-parametric test for dependent samples
# Equivalent to two-sample t test if the data is not normally distributed and ordinal; also applicable for small samples and outliers.
def mannwhitney(da1, da2, paired=False, dim="time", global_alpha=0.05):
    """xarray wrapper for Mann-Whitney U test
    Paramters
    ---------
    da1, da2 : xr.DataArray
        arrays of samples
    dim : str, default: "time"
        Dimension along which to compute the test
    global_alpha, float, default: 0.05
        Global alpha of Benjamini and Hochberg correction   
    
    """
    dim = [dim] if isinstance(dim, str) else dim

    def _mannwhitneyu(x, y):
        if paired: # if True
            return stats.wilcoxon(x, y, axis=-1, nan_policy="omit").pvalue
        else:
            return stats.mannwhitneyu(x, y, axis=-1, nan_policy="omit").pvalue

    # use xr.apply_ufunc to handle vectorization
    result = xr.apply_ufunc(
        _mannwhitneyu,
        da1,
        da2,
        input_core_dims=[dim, dim],
        output_core_dims=[[]],
        exclude_dims=set(dim),
        dask="parallelized",
        output_dtypes=[float],
    ).compute()

    # apply Benjamini and Hochberg correction
    shape = result.shape
    
    values = result.values.ravel()
    notnull = np.isfinite(values)

    p_adjust = multipletests(
        values[notnull], alpha=global_alpha, method="fdr_bh"
    )[0]
    values[notnull] = p_adjust
    result.values = values.reshape(shape)

    return result


# ------------------------------------------------------------
# Workflow for significance testing on xarray datasets using non-parametric tests
# Datasets can contain multiple variables, cases (paired or independent), seasons and regions
# FDR adjustment is applied across seasons and regions (variables and cases are treated as separate inferential families) 
# ------------------------------------------------------------

# Non-parametric significance tests: equivalent to t test if the data is not normally distributed and ordinal; also applicable for small samples and outliers.
# Wilcoxon rank-sum test: non-parametric test for dependent samples (two-sided)
# Mann-Whitney U rank test: non-parametric test for independent samples (two-sided)

# -------------------------------------------------------------------
# Test functions (reduce only along "dim")
# -------------------------------------------------------------------

def xr_wilcoxon(da, dim="time"):
    """
    Vectorized Wilcoxon signed-rank test across "dim".
    Returns test statistic, p-value, and effect size.
    Effect size: point‑biserial‑like/Pearson‑r‑like correlation r = Z / sqrt(n).
    """

    dim = [dim] if isinstance(dim, str) else dim

    def _wilcoxon(x):
        x = x[~np.isnan(x)]
        if x.size < 2:
            return np.nan, np.nan, np.nan
        
        res = stats.wilcoxon(x)
        W, p = res.statistic, res.pvalue

        n = x.size
        # Wilcoxon expected value and SD under H0
        mean_W = n * (n + 1) / 4
        sd_W   = np.sqrt(n * (n + 1) * (2*n + 1) / 24)

        z = (W - mean_W) / sd_W
        r = z / np.sqrt(n)
        return W, p, r

    W, p, r = xr.apply_ufunc(
        _wilcoxon,
        da,
        input_core_dims=[dim],
        output_core_dims=[[], [], []],
        vectorize=True,
        dask="parallelized",
        output_dtypes=[float, float, float],
    )

    return xr.Dataset({"statistic": W, "p": p, "effect_size": r})


def xr_mannwhitneyu(da1, da2, dim="time"):
    """
    Vectorized Mann–Whitney U test across "dim".
    Returns test statistic, p-value, and effect size.
    Effect size: rank-biserial correlation r = 1 - 2U/(n1*n2).
    """

    dim = [dim] if isinstance(dim, str) else dim

    def _mw(x, y):
        x = x[~np.isnan(x)]
        y = y[~np.isnan(y)]
        if x.size == 0 or y.size == 0:
            return np.nan, np.nan, np.nan

        res = stats.mannwhitneyu(x, y)
        U, p = res.statistic, res.pvalue
        
        n1, n2 = x.size, y.size
        r = 1 - (2 * U) / (n1 * n2)
        return U, p, r

    U, p, r = xr.apply_ufunc(
        _mw,
        da1, da2,
        input_core_dims=[dim, dim],
        output_core_dims=[[], [], []],
        vectorize=True,
        dask="parallelized",
        output_dtypes=[float, float, float],
    )

    return xr.Dataset({"statistic": U, "p": p, "effect_size": r})

# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

# Benjamini and Hochberg correction for multiple simultaneous tests (for ND arrays)
def multitest_bh(pvals):
    """
    Benjamini–Hochberg FDR correction on an xarray.DataArray of p-values.
    - Stacks all dims, corrects, and unstacks back.
    - NaNs are ignored and preserved.
    - Returns a NEW DataArray with same shape/coords as input.
    """
    da = pvals.astype(float)
    stacked = da.stack(_all_dims=list(da.dims))
    flat = stacked.data
    if hasattr(flat, "compute"):  # dask array
        flat = flat.compute()
    flat = np.asarray(flat)
    mask = np.isfinite(flat)
    adj = flat.copy()
    if mask.any():
        adj[mask] = multipletests(flat[mask], method="fdr_bh")[1]
    stacked_adj = xr.DataArray(adj, coords=stacked.coords, dims=stacked.dims)
    unstacked = stacked_adj.unstack("_all_dims")
    return unstacked.transpose(*pvals.dims)

# Iterate groups for split_dim
def _iter_groups(da, split_dim, *, test_dim="time"):
    """
    Iterator over grouped subsets for a single split_dim (e.g., 'season').
    Yields: (labels_dict, subset_da)
      - If split_dim is None: yields ({}, da)
      - Else: checks that da[split_dim] is a coordinate on test_dim, and groups by it.
    """
    if split_dim is None:
        yield {}, da
        return

    if split_dim not in da.coords:
        raise ValueError(f"'{split_dim}' is not a coordinate on the DataArray.")
    if da[split_dim].dims != (test_dim,):
        raise ValueError(
            f"'{split_dim}' must be a coordinate defined on '{test_dim}', "
            f"but has dims {da[split_dim].dims}."
        )

    for key, sub in da.groupby(split_dim):
        # Convert key to a Python scalar if it's a 0D numpy/xarray type
        label = key.item() if hasattr(key, "item") else key
        yield {split_dim: label}, sub


# -------------------------------------------------------------------
# Xarray dataset integration (cases and variables are separate families)
# -------------------------------------------------------------------

def xr_significance(
    ds,
    *,
    test_dim="time",
    split_dim=None,                 # None | str; must be a coord on test_dim (e.g., "season")
    paired_samples=None,            # e.g., ["nfn-ssp1", "nfs-ssp1", "nac-ssp1"]
    independent_samples=None,       # e.g., [("recent","ssp1")]
    multitest=False                 # FDR per variable & per case across remaining dims
):
    """
    Run paired (Wilcoxon) and independent (MWU) tests in one call, with at most one split dimension.
    The split dimension must be a time-aligned coordinate (dims == (test_dim,)).

    Output dims typically: ['variable', 'case', *other non-time dims*, split_dim?]
    Variables: ['statistic', 'p', 'effect_size']
    """

    if (not paired_samples) and (not independent_samples):
        raise ValueError("Provide at least one of `paired_samples` or `independent_samples`.")
    if "case" not in ds.dims:
        raise ValueError("Dataset must have a 'case' dimension to select cases.")

    results = []

    for var in ds.data_vars:
        da_full = ds[var]
        blocks = []

        # ---------- Paired ----------
        if paired_samples:
            for case_label in paired_samples:
                # Select and DROP the 'case' dimension so we can add it later cleanly
                da_case = da_full.sel(case=case_label, drop=True)

                sub = []
                for labels, da_g in _iter_groups(da_case, split_dim, test_dim=test_dim):
                    res = xr_wilcoxon(da_g, dim=test_dim)

                    # Attach split coord back as a size-1 dimension for clean concat
                    for name, val in labels.items():
                        res = res.expand_dims({name: [val]})

                    # And attach the 'case' dimension we removed earlier
                    res = res.expand_dims(case=[case_label])
                    sub.append(res)

                blocks.append(sub[0] if len(sub) == 1 else xr.combine_by_coords(sub, combine_attrs="drop"))

        # ---------- Independent ----------
        if independent_samples:
            for (c1, c2) in independent_samples:
                da1 = da_full.sel(case=c1, drop=True)
                da2 = da_full.sel(case=c2, drop=True)

                sub = []
                for labels, da1_g in _iter_groups(da1, split_dim, test_dim=test_dim):
                    # Align da2 to the time subset used by da1_g after grouping
                    da2_g = da2.sel({test_dim: da1_g[test_dim]})

                    res = xr_mannwhitneyu(da1_g, da2_g, dim=test_dim)

                    for name, val in labels.items():
                        res = res.expand_dims({name: [val]})
                    res = res.expand_dims(case=[f"{c1}-{c2}"])
                    sub.append(res)

                blocks.append(sub[0] if len(sub) == 1 else xr.combine_by_coords(sub, combine_attrs="drop"))

        if not blocks:
            continue

        # Concatenate all cases for this variable
        var_out = xr.concat(blocks, dim="case", coords="all")

        # FDR per variable & per case
        if multitest:
            var_out["p"] = var_out["p"].groupby("case").map(multitest_bh)

        # Attach variable for outer concat across variables
        results.append(var_out.expand_dims(variable=[var]))

    if not results:
        raise ValueError("No tests were produced. Check cases/pairs and split settings.")

    return xr.concat(results, dim="variable", coords="all")


# Encode significance levels with stars( for arrays)
def encode_significance(p_da: xr.DataArray, *, nan_label: str = "") -> xr.DataArray:
    """
    Encode p-values to significance stars with strict thresholds:
        "***" for p < 0.01
        "**"  for 0.01 <= p < 0.05
        "*"   for 0.05 <= p < 0.10
        ""    for p >= 0.10 or NaN  (can override with `nan_label`)
    """

    # Thresholds = four regions; np.digitize will return indices 0..3
    # With right=False: bins[i-1] < x <= bins[i] is FALSE; we get:
    #   idx=0: x < 0.01
    #   idx=1: 0.01 <= x < 0.05
    #   idx=2: 0.05 <= x < 0.10
    #   idx=3: x >= 0.10
    bins = np.array([0.01, 0.05, 0.10], dtype=float)
    stars_map = np.array(["***", "**", "*", ""], dtype=object)

    def _encode_array(x):
        # x is a NumPy array (not dask) here due to apply_ufunc wrapping
        x = np.asarray(x, dtype=float)
        out = np.full(x.shape, nan_label, dtype=object)
        m = np.isfinite(x)
        if m.any():
            idx = np.digitize(x[m], bins, right=False)  # 0..3
            out[m] = stars_map[idx]
        return out

    return xr.apply_ufunc(
        _encode_array,
        p_da,
        vectorize=True,
        dask="parallelized",
        output_dtypes=[object],
    )


# Format p-values (labeling rule)
def _format_pvalue_scalar(p, *, nan_label=""):
    if np.isnan(p):
        return nan_label
    return "P < 0.001" if p < 0.001 else f"P = {p:.3f}"

def format_pvalue_da(p_da: xr.DataArray, *, nan_label: str = "") -> xr.DataArray:
    return xr.apply_ufunc(
        lambda x: np.vectorize(_format_pvalue_scalar)(x, nan_label=nan_label),
        p_da,
        vectorize=True,
        dask="parallelized",
        output_dtypes=[object],
    )


# Summarize statistics: pulls statistic, p, and effect_size from the stat dimension
# Uses encode_significanc(p) to get the stars and the p-labeling rule
# Optional blanking for absolute values in some cases (e.g., "recent", "ssp1")
def format_stat_strings(
    da: xr.DataArray,
    *,
    stat_dim: str = "stat",
    stat_key: str = "statistic",
    p_key: str = "p",
    eff_key: str = "effect_size",
    stat_fmt: str = ".4g",
    eff_fmt: str = ".2g",
    nan_label: str = "",
    case_dim: str = "case",
    blank_cases: list[str] | None = None,
) -> xr.DataArray:
    """
    Produce strings like:
      "** (statistic = {stat}, P = {p or 'P < 0.001'}, effect size = {eff})"
    """
    if stat_dim not in da.dims:
        raise ValueError(f"`stat_dim='{stat_dim}'` not found in DataArray dims: {da.dims}")

    stat = da.sel({stat_dim: stat_key})
    p    = da.sel({stat_dim: p_key})
    eff  = da.sel({stat_dim: eff_key})

    # stars from YOUR encoding
    stars = encode_significance(p)

    # p label with "< 0.001" rule
    p_str = format_pvalue_da(p, nan_label=nan_label)

    def _format_scalar(a, ptxt, c, s):
        # Blank if any numeric component missing or p label missing
        if np.isnan(a) or (ptxt == nan_label) or np.isnan(c):
            return nan_label
        prefix = (s + " ") if s else ""
        return f"{prefix}(statistic = {a:{stat_fmt}}, {ptxt}, effect size = {c:{eff_fmt}})"

    strings = xr.apply_ufunc(
        _format_scalar,
        stat, p_str, eff, stars,
        input_core_dims=[[], [], [], []],
        output_core_dims=[[]],
        vectorize=True,
        dask="parallelized",
        output_dtypes=[object],
    )

    if blank_cases:
        if case_dim in strings.coords:
            case_vals = strings.coords[case_dim]
            mask = xr.DataArray(
                np.isin(case_vals, blank_cases),
                dims=(case_dim,),
                coords={case_dim: case_vals},
            )
            strings = xr.where(mask, nan_label, strings)

    out_dims = [d for d in da.dims if d != stat_dim]
    return strings.transpose(*out_dims)

# Summarize statistics on DataSet
def summarize_stat_dim(
    ds: xr.Dataset,
    *,
    stat_dim: str = "stat",
    stat_key: str = "statistic",
    p_key: str = "p",
    eff_key: str = "effect_size",
    stat_fmt: str = ".4g",
    eff_fmt: str = ".2g",
    nan_label: str = "",
    case_dim: str = "case",
    blank_cases: list[str] | None = None,
) -> xr.Dataset:
    """
    Apply `format_stat_strings` to each data variable with a `stat` dimension.
    Returns a string Dataset with `stat` removed.
    """
    out_vars = {}
    for name, da in ds.data_vars.items():
        if stat_dim not in da.dims:
            raise ValueError(f"Variable '{name}' lacks required stat dimension '{stat_dim}'.")
        out_vars[name] = format_stat_strings(
            da,
            stat_dim=stat_dim,
            stat_key=stat_key,
            p_key=p_key,
            eff_key=eff_key,
            stat_fmt=stat_fmt,
            eff_fmt=eff_fmt,
            nan_label=nan_label,
            case_dim=case_dim,
            blank_cases=blank_cases,
        )

    sample_var = next(iter(out_vars))
    return xr.Dataset(
        out_vars,
        coords={k: v for k, v in ds.coords.items() if k in out_vars[sample_var].coords},
    )