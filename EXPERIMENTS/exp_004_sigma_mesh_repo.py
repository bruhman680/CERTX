#!/usr/bin/env python3
"""
EXPERIMENT 004: σ_Mesh Measurement on Real Repositories
========================================================
Tests the CERTX σ_Mesh metric against real collaborative
software projects using only git history — no API cost.

σ_Mesh = 1 - r_network
Where r_network is the clustering coefficient of the
contributor-collaboration graph.

Healthy range: σ_Mesh ∈ [0.30, 0.50]
  - Too low:  over-coupled, no domain separation
  - Too high: siloed, no knowledge transfer

Requires:
  pip install pydriller networkx

Optional (for semantic drift analysis):
  pip install sentence-transformers

Usage:
  python exp_004_sigma_mesh_repo.py /path/to/local/repo
  python exp_004_sigma_mesh_repo.py https://github.com/owner/repo
  python exp_004_sigma_mesh_repo.py repo1 repo2 repo3  # comparison sweep
  python exp_004_sigma_mesh_repo.py --demo               # run on CERTX itself
"""

import sys
import math
import collections
import argparse
import os

# ─────────────────────────────────────────────
# Optional imports with graceful fallbacks
# ─────────────────────────────────────────────

try:
    from pydriller import Repository
    HAS_PYDRILLER = True
except ImportError:
    HAS_PYDRILLER = False

try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    HAS_SBERT = True
except ImportError:
    HAS_SBERT = False


# ─────────────────────────────────────────────
# Git history mining
# ─────────────────────────────────────────────

def mine_commits(repo_path, max_commits=500):
    """
    Walk git history and build:
      - file_authors: file → set of contributors who touched it
      - author_files: contributor → set of files they touched
      - commit_messages: list of commit messages (for semantic analysis)
    """
    file_authors = collections.defaultdict(set)
    author_files = collections.defaultdict(set)
    commit_messages = []
    commit_count = 0

    print(f"  Mining up to {max_commits} commits from {repo_path}...")

    try:
        for commit in Repository(repo_path).traverse_commits():
            commit_messages.append(commit.msg[:200].strip())
            author = commit.author.name or "unknown"
            for f in commit.modified_files:
                if f.filename:
                    file_authors[f.filename].add(author)
                    author_files[author].add(f.filename)
            commit_count += 1
            if commit_count % 200 == 0:
                print(f"    {commit_count} commits processed...")
            if commit_count >= max_commits:
                break
    except Exception as e:
        print(f"  WARNING: Mining stopped early — {e}")

    print(f"  Done: {commit_count} commits | "
          f"{len(author_files)} contributors | "
          f"{len(file_authors)} files")

    return file_authors, author_files, commit_messages


# ─────────────────────────────────────────────
# Network construction and σ_Mesh
# ─────────────────────────────────────────────

def compute_sigma_mesh_networkx(file_authors, author_files):
    """Compute σ_Mesh via NetworkX clustering coefficient."""
    G = nx.Graph()
    contributors = list(author_files.keys())
    G.add_nodes_from(contributors)

    for authors in file_authors.values():
        author_list = list(authors)
        for i in range(len(author_list)):
            for j in range(i + 1, len(author_list)):
                a, b = author_list[i], author_list[j]
                if G.has_edge(a, b):
                    G[a][b]['weight'] += 1
                else:
                    G.add_edge(a, b, weight=1)

    n = G.number_of_nodes()
    if n < 2:
        return {
            "sigma_mesh": 0.0,
            "r_network": 1.0,
            "avg_clustering": 1.0,
            "density": 1.0,
            "n_contributors": n,
            "n_files": len(file_authors),
            "n_edges": 0,
            "avg_degree": 0.0,
            "method": "networkx_clustering",
            "note": "solo repo — σ_Mesh undefined (single contributor = fully coupled)",
        }

    avg_clustering = nx.average_clustering(G)
    density = nx.density(G)
    degrees = [d for _, d in G.degree()]
    avg_degree = sum(degrees) / len(degrees) if degrees else 0

    # r_network: clustering coefficient is our order-parameter analog
    # High clustering = contributors are well-meshed (like Kuramoto r→1)
    # Low clustering  = siloed (like Kuramoto r→0)
    r_network = avg_clustering
    sigma_mesh = 1.0 - r_network

    return {
        "sigma_mesh": sigma_mesh,
        "r_network": r_network,
        "avg_clustering": avg_clustering,
        "density": density,
        "n_contributors": n,
        "n_files": len(file_authors),
        "n_edges": G.number_of_edges(),
        "avg_degree": avg_degree,
        "method": "networkx_clustering",
    }


def compute_sigma_mesh_manual(file_authors, author_files):
    """Fallback σ_Mesh via graph density (no networkx needed)."""
    contributors = list(author_files.keys())
    n = len(contributors)
    if n < 2:
        return {
            "sigma_mesh": 0.0,
            "r_network": 1.0,
            "density": 1.0,
            "n_contributors": n,
            "n_files": len(file_authors),
            "n_shared_pairs": 0,
            "method": "density_approx (install networkx for full analysis)",
            "note": "solo repo — σ_Mesh undefined (single contributor = fully coupled)",
        }

    # Count unique co-author pairs
    pairs = set()
    for authors in file_authors.values():
        lst = list(authors)
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                pairs.add((min(lst[i], lst[j]), max(lst[i], lst[j])))

    max_pairs = n * (n - 1) / 2
    density = len(pairs) / max_pairs

    # Approximate r from density (density ≈ r² for random graphs)
    r_approx = math.sqrt(density)
    sigma_mesh = 1.0 - r_approx

    return {
        "sigma_mesh": sigma_mesh,
        "r_network": r_approx,
        "density": density,
        "n_contributors": n,
        "n_files": len(file_authors),
        "n_shared_pairs": len(pairs),
        "method": "density_approx (install networkx for full analysis)",
    }


def compute_sigma_mesh(file_authors, author_files):
    if HAS_NETWORKX:
        return compute_sigma_mesh_networkx(file_authors, author_files)
    else:
        return compute_sigma_mesh_manual(file_authors, author_files)


# ─────────────────────────────────────────────
# Temporal σ_fiber via commit message drift
# ─────────────────────────────────────────────

def compute_temporal_sigma_fiber(commit_messages, window=50):
    """
    Semantic drift of commit messages over time.
    Requires sentence-transformers.

    Returns σ_fiber_temporal = std of rolling cosine similarity
    to the founding-purpose embedding (first `window` commits).
    """
    if not HAS_SBERT:
        return None
    if len(commit_messages) < window * 2:
        return None

    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("  Embedding commit messages (sentence-transformers)...")
    embeddings = model.encode(commit_messages, show_progress_bar=False)

    # Founding-purpose vector: mean of first `window` commit embeddings
    baseline = embeddings[:window].mean(axis=0)
    baseline_norm = baseline / (np.linalg.norm(baseline) + 1e-9)

    # Rolling window similarity to baseline
    similarities = []
    for i in range(window, len(embeddings)):
        win_emb = embeddings[max(0, i - window):i].mean(axis=0)
        win_norm = win_emb / (np.linalg.norm(win_emb) + 1e-9)
        sim = float(np.dot(baseline_norm, win_norm))
        similarities.append(sim)

    sigma_temporal = float(np.std(similarities))
    mean_drift = float(1.0 - np.mean(similarities))

    return {
        "sigma_fiber_temporal": sigma_temporal,
        "mean_purpose_drift": mean_drift,
        "n_windows": len(similarities),
    }


# ─────────────────────────────────────────────
# Interpretation
# ─────────────────────────────────────────────

def interpret_sigma_mesh(sigma):
    if sigma < 0.20:
        return "OVER-COUPLED: contributors fully entangled, no domain separation"
    elif sigma < 0.30:
        return "APPROACHING HEALTHY: slight over-coupling"
    elif sigma <= 0.50:
        return "HEALTHY RANGE [0.30-0.50]: domain separation + cross-pollination"
    elif sigma <= 0.70:
        return "UNDER-COUPLED: siloed domains, limited knowledge transfer"
    else:
        return "FRAGMENTED: contributors barely overlap, high silo risk"


def interpret_sigma_fiber(sigma, drift):
    if sigma < 0.05 and drift < 0.05:
        return "RIGID: project purpose almost never shifts"
    elif drift < 0.10:
        return "STABLE: purpose consistent, healthy"
    elif drift < 0.20:
        return "EVOLVING: normal scope expansion"
    else:
        return "DRIFTING: significant purpose shift over project lifetime"


# ─────────────────────────────────────────────
# Main scan function
# ─────────────────────────────────────────────

def scan_repo(repo_path, max_commits=500, with_semantic=True):
    """Scan a single repo and return all CERTX metrics."""
    print()
    print("=" * 65)
    print(f"σ_Mesh REPO SCAN")
    print(f"  Repo:    {repo_path}")
    print(f"  Commits: up to {max_commits}")
    print("=" * 65)

    # Mine
    file_authors, author_files, commit_messages = mine_commits(
        repo_path, max_commits=max_commits
    )

    if not author_files:
        print("  ERROR: no commits found.")
        return None

    # σ_Mesh
    print("\n  Building contributor network...")
    metrics = compute_sigma_mesh(file_authors, author_files)

    print()
    print("── NETWORK METRICS ──────────────────────────────────────────")
    print(f"  Contributors:   {metrics['n_contributors']}")
    print(f"  Files touched:  {metrics['n_files']}")
    if 'n_edges' in metrics:
        print(f"  Network edges:  {metrics['n_edges']}")
    print(f"  Graph density:  {metrics.get('density', 0):.4f}")
    if 'avg_clustering' in metrics:
        print(f"  Avg clustering: {metrics['avg_clustering']:.4f}  (= r_network)")
    if 'avg_degree' in metrics:
        print(f"  Avg degree:     {metrics['avg_degree']:.1f}")
    print(f"  Method:         {metrics.get('method', 'unknown')}")

    print()
    print("── CERTX σ_Mesh ─────────────────────────────────────────────")
    sigma = metrics['sigma_mesh']
    r = metrics['r_network']
    print(f"  r_network  = {r:.4f}")
    print(f"  σ_Mesh     = 1 - r = {sigma:.4f}")
    print()
    print(f"  → {interpret_sigma_mesh(sigma)}")

    # Temporal σ_fiber
    if with_semantic:
        if HAS_SBERT and len(commit_messages) >= 100:
            print()
            print("── TEMPORAL σ_fiber (commit message drift) ──────────────────")
            fiber = compute_temporal_sigma_fiber(commit_messages)
            if fiber:
                sf = fiber['sigma_fiber_temporal']
                drift = fiber['mean_purpose_drift']
                print(f"  σ_fiber_temporal = {sf:.4f}")
                print(f"  Mean purpose drift = {drift:.4f}  "
                      f"({fiber['n_windows']} windows)")
                print()
                print(f"  → {interpret_sigma_fiber(sf, drift)}")
                metrics['temporal_fiber'] = fiber
            else:
                print("  (need ≥100 commits for drift analysis)")
        elif not HAS_SBERT:
            print()
            print("  (skip semantic: install sentence-transformers for drift)")

    metrics['repo'] = repo_path
    metrics['commits_mined'] = len(commit_messages)
    return metrics


# ─────────────────────────────────────────────
# Comparison table
# ─────────────────────────────────────────────

def print_comparison(results):
    print()
    print("=" * 80)
    print("COMPARISON TABLE — σ_Mesh across repos")
    print("=" * 80)
    print(f"  {'Repo':<35} {'σ_Mesh':>8} {'r_net':>8} {'Contributors':>14} {'Files':>8}")
    print("  " + "─" * 77)
    for m in results:
        if m is None:
            continue
        name = m['repo'].rstrip('/').split('/')[-1][:34]
        sigma = m['sigma_mesh']
        r = m['r_network']
        n = m['n_contributors']
        nf = m['n_files']
        flag = "✓" if 0.30 <= sigma <= 0.50 else "↑" if sigma > 0.50 else "↓"
        print(f"  {name:<35} {sigma:>8.4f} {r:>8.4f} {n:>14} {nf:>8}  {flag}")
    print()
    print("  ✓ = healthy range (0.30–0.50)  ↑ = under-coupled  ↓ = over-coupled")


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Measure CERTX σ_Mesh on git repositories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python exp_004_sigma_mesh_repo.py --demo
  python exp_004_sigma_mesh_repo.py /path/to/repo
  python exp_004_sigma_mesh_repo.py https://github.com/numpy/numpy --commits 300
  python exp_004_sigma_mesh_repo.py repo1 repo2 repo3

Suggested sweep (popular repos):
  python exp_004_sigma_mesh_repo.py \\
    https://github.com/numpy/numpy \\
    https://github.com/scikit-learn/scikit-learn \\
    https://github.com/huggingface/transformers \\
    --commits 500
        """
    )
    parser.add_argument("repos", nargs="*", help="Repo path(s) or URL(s)")
    parser.add_argument("--commits", type=int, default=500,
                        help="Max commits to mine per repo (default: 500)")
    parser.add_argument("--no-semantic", action="store_true",
                        help="Skip semantic drift analysis")
    parser.add_argument("--demo", action="store_true",
                        help="Run on CERTX repo (this repo) as quick demo")

    args = parser.parse_args()

    # Check requirements
    if not HAS_PYDRILLER:
        print("ERROR: pydriller not installed.")
        print("  pip install pydriller")
        sys.exit(1)

    if not HAS_NETWORKX:
        print("WARNING: networkx not installed — using density approximation.")
        print("  For full analysis: pip install networkx")
        print()

    # Determine repo list
    repos = list(args.repos)
    if args.demo or not repos:
        # Default: run on this repo
        certx_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        repos = [certx_path]
        print(f"Demo mode: scanning CERTX repo at {certx_path}")

    # Scan
    results = []
    for repo in repos:
        result = scan_repo(repo,
                           max_commits=args.commits,
                           with_semantic=not args.no_semantic)
        if result:
            results.append(result)

    # Comparison table for multi-repo sweep
    if len(results) > 1:
        print_comparison(results)

    # Final summary
    print()
    print("─" * 65)
    print("NEXT STEPS")
    print("─" * 65)
    print()
    print("1. Run the suggested sweep to calibrate the healthy range:")
    print("   numpy (governance-strong) vs transformers (hypergrowth)")
    print()
    print("2. Compare σ_Mesh before/after a major version bump:")
    print("   git log --oneline | grep 'v2.0\\|v3.0' → find transition commit")
    print("   then --commits N from before vs after the pivot")
    print()
    print("3. Correlate σ_Mesh with CERTX ζ* claims:")
    print("   σ_Mesh ≈ 0.40 → r_network ≈ 0.60 → healthy partial sync")
    print("   This matches the Kuramoto C* zone from exp_003")
    print()
    if not HAS_SBERT:
        print("4. Install sentence-transformers for temporal σ_fiber:")
        print("   pip install sentence-transformers")
        print("   Then re-run for commit message drift analysis.")


if __name__ == "__main__":
    main()
