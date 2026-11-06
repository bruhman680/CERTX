# Independent Scheme reference

Chibi Scheme 0.12.0 is built and smoke-tested locally as an independent value-semantics oracle. It is not the prototype runtime, sandbox, or security oracle. No binary or source was added to this repository.

- Official source: <https://github.com/ashinn/chibi-scheme>
- Pinned tag: `0.12`; exact commit: `08e23be118e7de8cf29d606bc4793371c0ace680`.
- Version source: <https://github.com/ashinn/chibi-scheme/blob/08e23be118e7de8cf29d606bc4793371c0ace680/VERSION> (`0.12.0`).
- Language documentation: [official README](https://github.com/ashinn/chibi-scheme/blob/08e23be118e7de8cf29d606bc4793371c0ace680/README.md) describes R7RS-small support; [R7RS-small](https://small.r7rs.org/) supplies the broader language specification. The prototype implements only its documented subset.
- License: BSD 3-clause terms in [COPYING](https://github.com/ashinn/chibi-scheme/blob/08e23be118e7de8cf29d606bc4793371c0ace680/COPYING), retained in the local checkout.

GitHub connector metadata and official files were inspected before fetching source. The managed environment reported current, enforced unrestricted HTTP policy; its network-policy snapshot had no configured VPN. Fetching used inherited proxy/TLS settings and no credentials.

## Local build and invocation

Source checkout: `/workspace/world_blueprint_reference/chibi-scheme-0.12`.
Local install prefix: `/workspace/world_blueprint_reference/install`.
Built on Linux x86_64 with GCC `14.2.0` (Debian `14.2.0-19`) and GNU Make `4.4.1`:

```sh
git clone --depth 1 --branch 0.12 https://github.com/ashinn/chibi-scheme.git /workspace/world_blueprint_reference/chibi-scheme-0.12
git -C /workspace/world_blueprint_reference/chibi-scheme-0.12 rev-parse HEAD
make -C /workspace/world_blueprint_reference/chibi-scheme-0.12 -j2 PREFIX=/workspace/world_blueprint_reference/install
make -C /workspace/world_blueprint_reference/chibi-scheme-0.12 PREFIX=/workspace/world_blueprint_reference/install install
```

Build and local installation exited 0. Upstream installation attempted `ldconfig`, whose failure was ignored by its Makefile; the wrapper supplies the local library path and needs no system installation. Upstream's full test suite was not run.

Executable: `/workspace/world_blueprint_reference/install/bin/chibi-scheme`.
Convenient wrapper: `/workspace/world_blueprint_reference/chibi-reference`.
The wrapper sets `LD_LIBRARY_PATH` to the local prefix, `CHIBI_IGNORE_SYSTEM_PATH=1`, and `CHIBI_MODULE_PATH` to that prefix's Scheme modules. Run a trusted fixture with:

```sh
timeout 5 /workspace/world_blueprint_reference/chibi-reference /absolute/path/trusted.scm
```

A fixture can contain:

```scheme
(import (scheme base) (scheme write))
(define (factorial n)
  (if (= n 0) 1 (* n (factorial (- n 1)))))
(write (list (+ 2 3) (factorial 6)
             (string-append "hello" " world")
             (cons 1 (list 2 3))
             (equal? '(1 "x") (list 1 "x"))))
(newline)
```

Verified fixture: `/workspace/world_blueprint_reference/trusted-smoke.scm`.
Observed exit 0 and output: `(5 720 "hello world" (1 2 3) #t)`.
`chibi-reference -V` reports `chibi-scheme 0.12.0 "magnesium"`, including `r7rs`, full Unicode, ratios, complex numbers, and dynamic loading features.

## Limits

Use this external executable only for trusted, deliberately bounded fixtures. Chibi itself exposes modules, dynamic loading, files and process facilities; this build is not a hostile-code sandbox. Never pass raw model-generated guest programs to it. The prototype's no-host-import rule, capabilities, gas accounting, receipts, replay, and command behavior belong to the prototype and cannot be validated by this reference. Restrict differential cases to shared defined value semantics; avoid relying on unspecified argument evaluation order, error wording, implementation limits, or features outside the prototype subset. A timeout bounds elapsed time only and does not revoke host capabilities. Local checkout/install paths are session artifacts and are not portable dependencies; checks must report an unavailable oracle explicitly when absent.
