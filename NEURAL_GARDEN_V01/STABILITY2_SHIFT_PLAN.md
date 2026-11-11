# STABILITY2_SHIFT: predeclared abundance and severe seasonal-shock follow-up

**Research loop:** Determine whether the good behavior of tight trust-region constraints carries into a novel rich/scarce/rich resource regime and, crucially, ever beats the same-mode frozen trained neural controller.

## Design before outcomes

- Regrowth `.09` for first third, `.03` for middle third, `.09` for final third. This contrasts with the original `.06/.055/.06` and deliberately tests a large change, not a naturalistic ecology.
- All cells retain original energy law; initial world, pretraining and stochastic action streams paired by seed.
- Fresh development seeds `10500..10507`, reserved independent holdout `10600..10607`. Size 10×10, 1000 pretrain steps, 3000 evaluation steps. Analysis includes final energy/floor, mean raw drift over last 500 ticks, and middle-of-scarcity mean energy.
- Five arms: frozen pretrained policy; unrestricted online updater; online trust radius .025; online trust radius .10; **sham** trust radius .10 with within-world randomly permuted per-cell gradient increments each tick, a same-budget corruption of gradient assignment. Sham keeps baseline updates and projection budget, but does not preserve each cell's correct local learning signal. It is not equivalent to a perfectly random matched policy.
- Test paired held-out wins against frozen; only credit adaptive learning if updated learned policy surpasses frozen on unseen seeds. Compare radius .10 true local gradient vs sham to assess whether gradient directions matter.
- No zero-centered anchor sham from prior plan. No claim of automatic switch detection or long-term viability.
