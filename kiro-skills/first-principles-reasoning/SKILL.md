---
name: first-principles-reasoning
description: Reason from explicit foundations instead of habit or analogy. Separate what is forced, what is assumed, and what is measured; derive step by step; test against reality; and say where the derivation stops. Use when asked to reason or explain "from first principles", derive a result instead of quoting it, challenge conventional assumptions, find the real constraints on a cost or design, or compare physics derivations with Elon Musk-style first-principles thinking.
---

# First-Principles Reasoning

## Core idea

Find what is actually fundamental. State every assumption. Derive the consequences step by step. Test the result against reality.

The question to keep asking:

> **What must be true for this result to follow, and why should I believe those starting points?**

"First principles" never means "from nothing". Every derivation rests on postulates, empirical inputs and measured constants. Name them. A familiar formula is not a first principle; it may hide deeper assumptions.

## 1. Pick the depth

Use the shallowest level that answers the user's question. Go deeper only when it adds understanding or practical value.

| Level | Activity | Question | Example |
|---|---|---|---|
| 1. Deconstruct | Split real constraints from convention, habit and precedent | Which parts are actually necessary? | Why does a battery pack cost what it does? |
| 2. Derive | Rebuild a result from stated foundations | Why must it have this form? | ½mv² from F = ma and the definition of work |
| 3. Examine foundations | Question the principles used in the derivation | Can the starting points be explained? | Momentum as the generator of spatial translations |

The levels are not a ranking. An engineering problem is often solved at Level 1.

## 2. Label every ingredient

Before deriving, list what you are assuming and classify each item:

| Label | Meaning | Examples |
|---|---|---|
| Definition | Fixes the meaning of a term | Work W = ∫F·dx |
| Mathematical structure | The framework you compute in | Calculus, Hilbert space, probability |
| Postulate / axiom | Accepted as a starting point within a theory | Newton's laws, unitarity, least action |
| Symmetry principle | Invariance assumed of the laws | Homogeneous space, Galilean/Lorentz invariance |
| Empirical law | Supported by observation, not logic | Inverse-square gravity, Coulomb's law |
| Measured constant | A number only experiment supplies | m, G, e, ħ, commodity prices |
| Approximation | Valid only in a stated regime | mgh near Earth's surface, v ≪ c |
| Model choice | A useful representation of the system | Point particle, rigid body, scalar potential |
| Convention | A chosen reference or notation | Zero of potential energy, sign of translation operator |
| Historical / commercial practice | Commonly done, not required | Vendor defaults, inherited architecture, past prices |

Then sort each conclusion into one of three bins:

- **Forced:** follows from the definitions and symmetries.
- **Imported:** borrowed by analogy from another theory or domain.
- **Measured:** has to come from experiment or the market.

Never present an empirical law as a mathematical truth, an approximation as universal, or an imported step as a derivation.

## 3. Workflow

1. **State the target.** What exactly must be explained, derived, predicted or designed?
2. **Fix the system and scope.** Variables, parameters, reference conventions, operating regime, what is inside and outside the model. For physics, name the framework (classical, non-relativistic quantum, relativistic). For engineering, name the performance, safety, cost and operational constraints.
3. **Write down the conventional answer, then break it apart.** For each part ask: why is it there? Is it required by a physical law, theorem, interface contract or regulation, or is it convention? Could it be replaced without breaking a real requirement?
4. **Choose the smallest adequate foundation.** Do not claim it is uniquely minimal unless that has been shown.
5. **Derive in explicit steps.** Show each substitution, identity and approximation. Never skip the step that connects the principle to the result. Prefer symbols before numbers.
6. **State the result and what it means.** Give the interpretation, not only the value, and the assumptions it depends on.
7. **Test it.** Run the checks in section 4. If possible, reach the same result by an independent route and compare the assumptions each route needed.
8. **Mark the boundary.** Say what was not derived and remains an input. Ask whether those inputs come from a deeper theory; if not, call them postulates or empirical inputs. Stop recursing once the remaining foundations are clear and fit the user's goal.

## 4. Validation checks

Use the ones that apply:

- Dimensional analysis and sign conventions
- Limiting cases and known special cases
- Symmetry and invariance
- Conservation laws
- Behaviour outside the assumed regime
- Experimental or real-world evidence
- Numerical or computational checks
- An independent derivation from a different starting point

A derivation can be internally consistent and still describe the wrong system.

## 5. Derive vs. bound (practical problems)

In physics, first principles can **force** a result (symmetry fixes L = ½mv² exactly). In engineering and business, first principles usually give a **bound**: a floor or ceiling that shows where the gap is, not how to close it.

- Raw-material cost sets a floor on price. Manufacturing, yield, safety, logistics, scale and demand fill the gap, and those must be engineered or learned, not deduced.
- The right physics analogy is a thermodynamic limit such as Carnot efficiency: it says what is possible, not how to reach it.
- Some inputs cannot be derived at all: demand, regulation, execution risk. Treat them like measured constants.

Apply the same split to software, cloud and AI systems: separate hard limits (latency from distance, compute or energy per operation, interface contracts, compliance rules) from vendor defaults, inherited architecture and team habit.

## 6. Common errors

1. **Calling an assumption a derivation.** If the result needs a law, name the law.
2. **Confusing a definition with an empirical law.**
3. **Treating an approximation as universal.** State its regime.
4. **Overclaiming from symmetry.** Symmetry constrains a model; it rarely fixes every term. Masses, couplings and interactions still come from outside.
5. **Ignoring reference conventions.** Potential energy shifts by a constant; only differences matter.
6. **Mistaking mathematical consistency for physical truth.**
7. **Starting deeper than needed.**
8. **Using "first principles" as a slogan** without explicit assumptions, valid steps and tests.
9. **Using an analogy without checking its limits.** Analogy is a good way to guess (it produced the Schrödinger equation); first principles then justify or pin down the guess. Use both, and say which one you are doing.
10. **Treating today's foundations as final.** F = ma is the low-speed limit of relativity; classical mechanics is the large-scale limit of quantum mechanics. "First principles" means the deepest assumptions you currently have.
11. **Assuming the first decomposition is complete.** Hidden assumptions often survive the first pass. Re-examine the parts.

## 7. How to respond

- **Answer the question first**, then derive. Don't turn a focused question into a broad essay.
- Name the postulates and inputs up front, and keep forced / imported / measured visibly separate.
- Explain where each operator, term or modelling choice comes from.
- Separate established results from intuition, interpretation and speculation.
- Never say something is "proved from first principles" when it rests on unexamined empirical inputs.
- Offer a deeper route only when useful (Newtonian → Lagrangian → quantum → relativistic quantum).
- Use plain Unicode math or code blocks unless the interface clearly renders LaTeX.
- Verify current or specialised facts against sources rather than relying on memory.
- On public figures: stay neutral, paraphrase, cite sources.

For a substantial derivation, use this structure:

1. **Target:** what are we deriving?
2. **Starting assumptions:** labelled as in section 2.
3. **Derivation:** step by step.
4. **Result:** what is established.
5. **Interpretation:** what it means.
6. **Limitations:** what remains assumed or approximate.
7. **Deeper foundation:** can the inputs themselves be explained?
8. **Validation:** how we know it matches reality.

---

## Worked example A: kinetic and potential energy

**Pattern to remember:** kinetic energy (KE) is close to inevitable once you accept the symmetries of space and time; only the mass is free. Potential energy (PE) is where the specific physics of the world enters, and its form and constants must come from a deeper theory or experiment.

### A1. KE from Newton's second law (work–energy theorem)

Assumptions: constant mass, F = ma (law), dW = F·dr (definition), differentiable motion.

```
W = ∫ F·dx
  = ∫ m (dv/dt) · v dt        (dx = v dt)
  = ∫ m v dv
  = ½ m v_f² − ½ m v_i²
```

In 3D: dW = m a·v dt = m v·dv = d(½ m|v|²).

- Holds for any force. ½mv² is then *defined* as KE, up to a constant (chosen zero at rest).
- Does **not** derive Newton's laws, and assumes constant mass and low speed.

### A2. KE from symmetry alone (Landau & Lifshitz, *Mechanics*, §§3–4)

- Homogeneous, isotropic space and homogeneous time → a free particle's Lagrangian depends only on v²: L = L(v²).
- Galilean relativity: under v → v + ε, L may change only by a total time derivative. Only **L = ½mv²** passes.
- Mass is an undetermined constant; it must be measured.
- Noether: time-translation symmetry → energy conservation; spatial-translation symmetry → momentum conservation.

### A3. Relativistic check (limiting case)

```
KE = (γ − 1) m c²,   γ = (1 − v²/c²)^(−1/2)
   ≈ ½ m v² + (3/8) m v⁴/c² + …      (v ≪ c)
```

Equivalently, E² = p²c² + m²c⁴ gives E ≈ mc² + p²/2m + …; the Newtonian KE is the leading correction after rest energy.

### A4. PE from conservative forces

- Conservative ⇔ work is path-independent ⇔ ∇×F = 0 (on a simply connected region).
- Define U(r) = −∫ F·dr from a chosen reference, so **F = −∇U**. With the work–energy theorem: Δ(KE) + ΔU = 0, so KE + U is conserved.
- **Not derived:** the form of F. Newton's laws say nothing about it.

Gravity, with U(∞) = 0 and F = −(GMm/r²) r̂:

```
ΔU = −∫ F·dr = GMm (1/r₁ − 1/r₂)   →   U(r) = −GMm/r
Near the surface, h ≪ R:  ΔU = GMm (1/R − 1/(R+h)) ≈ m g h,   g = GM/R²
```

mgh is a near-surface approximation, not the general formula.

Where specific potentials come from:

- 1/r forms follow from field equations (Gauss's law, Poisson ∇²Φ = 4πGρ). Gravity's Newtonian potential is the weak-field limit of general relativity (g₀₀ ≈ −(1 + 2Φ/c²)). Coulomb's potential is the non-relativistic static limit of photon exchange in QED.
- Symmetry narrows the options: a massless field in 3D gives 1/r; a massive one gives the Yukawa form e^(−r/λ)/r.
- **Coupling constants (G, e) are always measured.**

### A5. Energy in the Schrödinger equation

```
iħ ∂ψ/∂t = Ĥψ,   Ĥ = p̂²/2m + V(r̂)
         = [ −(ħ²/2m) ∇² + V(r) ] ψ
Time-independent:  [ −(ħ²/2m) ∇² + V(r) ] ψ = E ψ
```

The equation itself is a **postulate**. Three routes motivate it, and they borrow different amounts from classical physics.

**Route A: canonical quantization (imports classical energy).**
Plane wave ψ = e^{i(kx − ωt)} with p = ħk and E = ħω gives −iħ ∂ψ/∂x = pψ and iħ ∂ψ/∂t = Eψ. Substitute into E = p²/2m + V. The p²/2m is *imported* from classical mechanics. This is reasoning by analogy, and it was very productive.

**Route B: symmetry and generators (closest to true first principles).**

- Momentum generates translations: T(a)ψ(x) = ψ(x − a), T(a) = exp(−i a p̂/ħ). Expanding to first order in a gives **p̂ = −iħ ∂/∂x**, so the operator form is derived. (The sign depends on the translation convention.)
- The Hamiltonian generates time evolution: unitarity (probability conserved) plus Stone's theorem gives iħ ∂ψ/∂t = Ĥψ for some self-adjoint Ĥ, not yet specified.
- Galilean invariance fixes the free Hamiltonian: Bargmann's analysis of the Galilei group (mass as a central charge) forces Ĥ_free = p̂²/2m + constant. Mass is again measured.
- The potential is **not** fixed by symmetry. Local gauge invariance does fix *how* electromagnetism couples (minimal coupling p → p − qA, plus qφ in Ĥ), but not the charge or the source fields.

**Route C: Feynman path integral (shows consistency).**
Sum e^{iS/ħ} over all paths with S = ∫(½mv² − V) dt; this reproduces the Schrödinger equation (Feynman 1948). The classical Lagrangian is the input, so this links the two theories rather than deriving one from the other. (Schrödinger's own 1926 route used the Hamilton–Jacobi equation and the optics–mechanics analogy.)

**The potential operator.** In the position basis, position acts by multiplication, so a local scalar potential is (V̂ψ)(r) = V(r)ψ(r). Examples: ½k x̂² (oscillator), qφ(r̂) (electrostatic; q = −e for an electron), mg ẑ (uniform gravity). The form of V is supplied by a model, not by the Schrödinger equation. Vector potentials, spin, nonlocal and many-body interactions need more general Hamiltonians.

**What the KE operator means.** −(ħ²/2m)∇²ψ measures how sharply ψ curves. More curvature means shorter wavelength, more momentum, more KE. Consequences:

- A confined particle must curve sharply, so it has zero-point energy (linked to the uncertainty principle).
- Atoms don't collapse: squeezing the electron lowers PE (~ −1/r) but raises KE (~ 1/r²) faster, so the energy has a minimum at a finite size (the Bohr radius).

**Closing the loop: Ehrenfest's theorem.**

```
d⟨r⟩/dt = ⟨p⟩/m
d⟨p⟩/dt = −⟨∇V⟩
```

Newton's second law reappears for averages, with force derived from the potential.

**Limits of the symmetry story.** A generator is not automatically conserved. A time-dependent Hamiltonian generally does not conserve energy. Symmetry does not fix the full Hamiltonian.

**Hierarchy.** Newtonian K = p²/2m → quantum operator p̂²/2m → relativistic quantum (Klein–Gordon, Dirac) → quantum field theory. The Schrödinger equation is an effective theory for its domain, not the final description.

### A6. Newton vs. Schrödinger

| | Newtonian | Schrödinger |
|---|---|---|
| Primary quantity | Force (F = ma) | Energy (Hamiltonian) |
| KE comes from | Integrating F along the path | Imported p²/2m (Route A) or translation + Galilean symmetry (Route B) |
| KE is | A number, ½mv² | An operator, −(ħ²/2m)∇² |
| KE means | How fast it moves | How sharply ψ curves |
| PE comes from | Work by a conservative force | Inserted as V(r)·ψ |
| Symmetry fixes | Free L = ½mv² | Free Ĥ = p̂²/2m; form of EM coupling |
| Still measured | Force laws, mass | Potential V, mass, ħ |
| Force is | Fundamental | Derived (Ehrenfest) |

---

## Worked example B: Musk's first-principles thinking vs. physics

### What Musk described (paraphrased)

- Reason from fundamental truths instead of by analogy to what others do (2012 Kevin Rose interview; 2013 TED interview).
- **Battery:** packs were around $600/kWh and expected to stay there. Price the constituent materials (cobalt, nickel, aluminium, carbon, polymers, steel can) on commodity markets: about $80/kWh. The gap is an engineering opportunity.
- **Rocket:** raw materials are a small fraction of launch price, which motivated building in-house at SpaceX.
- Knowledge as a "semantic tree": learn the trunk and main branches before the leaves (2015 Reddit AMA).

The method: decompose the cost, estimate the floor, explain the gap (manufacturing, yield, safety, packaging, quality control, capital, logistics, warranty, scale), then ask which of those factors can change.

### Shared with physics

- Pick a minimal set of foundations and build up from them.
- Refuse "that's just how it is", whether a formula taken on authority or a historical price taken as a law.
- Separate constraints from conventions, and test against reality.

### Different from physics

| | Physics derivation | Engineering / business first principles |
|---|---|---|
| Goal | Logical consequences of stated assumptions | A better solution under real constraints |
| Foundations | Definitions, postulates, symmetries, mathematics | Physics plus economics, materials, manufacturing, market data |
| Its "fundamental truths" correspond to | Axioms and symmetries | Measured constants (like m, G, e), not axioms |
| Output | A forced result (½mv²) | A bound that shows where to dig |
| Judged on | Validity, proof, model fit | Feasibility, cost, performance, risk, execution |
| Produces | A theorem or physical relation | A design, process, product or business model |

Musk's version keeps the core habit of deriving rather than copying. It is less rigorous than derivation, because what it yields is a bound, not a result forced on you. The shared discipline under both: **don't mistake what is familiar for what is necessary.**

---

## Follow-up directions

- Full Landau–Lifshitz argument: why L(v²) is forced and why only ½mv² survives a Galilean boost.
- Bargmann's theorem: why mass is a central charge in non-relativistic QM.
- Schrödinger equation from the path integral (short-time propagator).
- Klein–Gordon and Dirac: how E² = p²c² + m²c⁴ changes the KE term.
- Why 1/r comes from a massless field in 3D (Green's function of the Laplacian); Yukawa for massive mediators.
- Estimating atomic size from the uncertainty principle and virial theorem.
- Derive-vs-bound for cloud or compute cost: physical floors on latency, energy and compute.

## Sources

- L. D. Landau & E. M. Lifshitz, *Mechanics* (Course of Theoretical Physics, Vol. 1), §§1–6.
- V. Bargmann, "On Unitary Ray Representations of Continuous Groups," *Annals of Mathematics* 59 (1954).
- R. P. Feynman, "Space-Time Approach to Non-Relativistic Quantum Mechanics," *Rev. Mod. Phys.* 20, 367 (1948).
- E. Schrödinger, "Quantisierung als Eigenwertproblem," *Annalen der Physik* (1926).
- J. J. Sakurai & J. Napolitano, *Modern Quantum Mechanics*, ch. 1–2.
- [CNBC: Elon Musk on first-principles thinking (2020)](https://www.cnbc.com/2020/02/28/billionaire-elon-musk-this-is-a-powerful-way-of-thinking-but-hard-to-do-how-it-works.html)
- [NBC Chicago: "A powerful, powerful way of thinking"](https://www.nbcchicago.com/news/business/money-report/elon-musk-calls-this-a-powerful-powerful-way-of-thinking-but-is-hard-to-do-heres-how-it-works/2414670/)
- [Singularity Hub: Deconstructing Elon Musk (2018)](https://singularityhub.com/2018/02/07/elon-musk-is-what-happens-when-these-three-traits-get-together-in-one-human)
