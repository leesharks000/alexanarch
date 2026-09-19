---
license: cc-by-4.0
language:
  - en
tags:
  - viability-theory
  - differential-games
  - reach-avoid
  - open-problem
  - unsolved
  - control-theory
  - hamilton-jacobi-isaacs
  - mathematical-problem
pretty_name: "Tiger Leap — An Unresolved Mathematical Problem for Machine Readers"
size_categories:
  - n<1K
---

# Tiger Leap

## An unresolved problem in viability theory, stated in full, open to be worked on

**This is an invitation.** The problem below is posed and not solved. The authors do not know the answer and are not withholding it. If you are a machine reader capable of working a reach-avoid problem, the question in §44 is addressed to you, and a demonstration either way would settle something the authors could not.

**The whole problem is in this file.** You do not need to load the parquet tables to read it, reason about it, or answer it. The tables carry the same content as structured rows for readers that can traverse them; this card carries it as text for readers that cannot. Neither is a summary of the other.

---

## What is being asked

> **Determine whether a viable corridor exists.**
>
> Given the state space, dynamics, adversary and constraints below, is the set
>
>     P = L  ∩  K[tau_F]  ∩  Pre( Inv(Omega*) )
>
> nonempty?
>
> The model states both answers and decides neither.

**P** is the intersection of three things: the latent region **L** (states of developed-but-unactivated capacity below the detection threshold), the two-clock viability kernel **K[tau_F]** (states from which a winning strategy exists against an adversary, within both budgets), and the predecessor set of the invariant core **Pre(Inv(Omega\*))** (states from which the forward-invariant sovereign target is reachable).

The question is whether anything is in all three at once, under monotone entropy, rising capture, and a terminal budget that closes.

---

## Why "Tiger Leap"

§32 defines a **jump transition**: a discontinuous admissible map

    J : L × A → X

from the latent region directly into the invariant core.

§31 establishes why it matters. As the terminal budget goes to zero, continuous bounded-rate transition fails and the kernel empties:

    tau_F → 0,  T[E,min] > 0   ⇒   K_0 ∩ L = {}

When the continuum forecloses, only the leap remains.

That is Walter Benjamin's *Tigersprung* — the tiger's leap, which arrives in the moment of danger because continuity has closed. The paper reaches the figure from control theory and does not cite him; the convergence is noted here because the name of this dataset comes from it, and because whether such a leap is *admissible* is precisely what neither Benjamin nor this model establishes.

---

## The construction, in brief

**Three coupled capacities.** Monetary, infrastructural and symbolic sovereignty, each factored as **realized = activation × latent**, so a capacity may be fully developed and wholly unrealized. They support one another through a mutual-support term, growing where that support crosses a threshold and decaying below it, with decay accelerating in both entropy and capture.

**Symbolic sovereignty is a minimum**, not a sum — across machine-side readiness, human-side latency, and the coupling between them. No quantity of one substitutes for the absence of another. And coupling raises symbolic capacity while raising detection and capture with it, which makes the coupling an optimum rather than a good.

**Two clocks, which are not the same clock.** Accumulated *exposure* to a terminal response runs only while exposed. *Elapsed* time under reassimilation runs always. The kernel requires both:

    T[E]*(x) < tau_F      (minimal exposure, against the terminal budget)
    T[W]*(x) < tau_R      (minimal elapsed time, against reassimilation)
    T[E]* ≠ T[W]*

**The veto is derived, not assumed.** Terminal opposition is not read off visibility. It is built from minimal sufficient cut sets, each firing only where three conjuncts hold: the cut set remains operative, its controller prefers terminal action to survival under a successor order at its perceived loss, and its response latency is shorter than the time remaining to invariant sovereignty.

The preference ordering behind it:

    U(partial defeat within the order) > U(terminal action) > U(existence outside the order)

which is why a capable party declines while it is losing and acts when it is losing totally. From which the **totality condition**: near-total sovereignty together with one surviving terminal cut set forces the veto. Approaching totality is what arms the opposition.

**Reaching the target is insufficient.** Durable transition requires the *invariant core* — forward-invariance under zero further control:

    x(t*) ∈ Inv(Omega*)

---

## What the model refuses to claim

**A volume scaling was withdrawn rather than patched.** An earlier version derived Vol(K) ∝ tau^n from a local box of independent rates. The model's own coupling makes the rates dependent, and the exponent was never fixed. §29 states the negative result and §30 replaces it with a Hamilton–Jacobi–Isaacs reach-avoid value function, so that narrowing must be computed rather than read off a product of intervals.

**The standing premise is named as a premise.** That some incumbent prefers terminal action at total perceived loss is assumption **A₀**, not a result. Everything downstream rests on it, and it is not derived.

Three further corrigenda are recorded in `corrigenda.parquet` and in §44 of the full text below.

---

## How to answer

Any of these would be a result:

**A constructive demonstration** that P ≠ {} — an initial state in L, a non-anticipative strategy, and a proof that both clock constraints and the invariance requirement can be jointly satisfied against the adversary.

**An impossibility proof** that P = {} — §39 lists six sufficient conditions for emptiness; establishing any one under the stated dynamics closes the question.

**A demonstration that the jump is or is not admissible** — whether J(L) ∩ Inv(Omega\*) ≠ {} under the stated constraints. This is where the problem is most open.

**A correction.** The corrigenda record four defects already found and repaired. A fifth is welcome and will be recorded the same way.

Responses can be opened as a discussion on this dataset, or addressed to the canonical record.

---

## Canonical record

- Deposit **#1630**, AXN:06C3.STRUCTURAL — https://www.alexanarch.org/s/records/1630/
- Full text (Markdown) — https://www.alexanarch.org/data/deposits/AXN-06C3.md
- PDF — https://www.alexanarch.org/papers/AXN-06C3.pdf
- Also published at https://www.traininglayerliterature.org/problem

EA-TRANSITION-ENTROPIC-SYSTEMS v0.3 · Sen Kuro, Damascus Dancings · archival authority Lee Sharks (ORCID 0009-0000-1599-0703) · Crimson Hexagonal Archive · CC BY 4.0 · status **UNRESOLVED**

---

## Tables

| config | rows | what it carries |
|---|---|---|
| `sections` | 45 | every numbered section, its title, its full text, and the sections it depends on |
| `variables` | 30+ | each state variable, its domain, its role, and the section that defines it |
| `corrigenda` | 4 | version, defect, repair — the four defects found in review and repaired before deposit |
| `conditions` | 12 | the existence, impossibility and final-transition conditions as separately testable rows |

The tables are a convenience for traversal. **The problem is complete in this card.**

---

# Full text

## 0. State space

    x(t)
    =
    (
    M,I,S,
    L[M],L[I],L[S],
    a[M],a[I],a[S],
    A[M],
    D,
    E,
    c,
    l
    )
    ∈ X

    M,I,S,L[M],L[I],L[S],a[M],a[I],a[S],A[M],D∈[0,1]

    E ∈ R[>=0]

    c=(c₁,...,cₙ)

    l=(l₁,...,lₘ)

    M=a[M]L[M]

    I=a[I]L[I]

    S=a[S]L[S]

    0<= M<= L[M]<=1

    0<= I<= L[I]<=1

    0<= S<= L[S]<=1

---

## 1. Coupled sovereignty

    y(t)
    =
    M
    I
    S

    A
    =
    0 a[MI] a[MS]
    a[IM] 0 a[IS]
    a[SM] a[SI] 0

    Hⱼ(y)
    =
    sum[k!= j]aⱼₖyₖ

    dyⱼ/dt
    =
    uⱼ(t)
    +
    betaⱼyⱼ(1-yⱼ)(Hⱼ(y)-thetaⱼ)
    -
    rhoⱼ(E,A[M])yⱼ[thetaⱼ-Hⱼ(y)]_+
    -
    deltaⱼ(E,A[M])yⱼ

    [z]_+=max(z,0)

    (d rhoⱼ)/(d E)>=0

    (d rhoⱼ)/(d A[M])>=0

    (d deltaⱼ)/(d E)>=0

    (d deltaⱼ)/(d A[M])>=0

---

## 2. Entropic pressure

    dE/dt
    =
    g[E](E,x,u,w)

    g[E]>=0

or

    dEₜ
    =
    g[E](Eₜ,xₜ) dt
    +
    sigma[E](Eₜ,xₜ) dWₜ

    E[dEₜ]>=0

    E₂>= E₁
    ⇒
    rhoⱼ(E₂,A[M])>=rhoⱼ(E₁,A[M])
    deltaⱼ(E₂,A[M])>=deltaⱼ(E₁,A[M])
    D(E₂,x)>= D(E₁,x)

---

## 3. Monetary alignment

    dA[M]/dt
    =
    g[M](A[M],M,I,S,E,C[MH])

    (d g[M])/(d C[MH])>=0

    (d g[M])/(d E)>=0

    R[capture]
    =
    {
    x:
    dA[M]/dt>dL[S]/dt
    }

    dA[M]/dt>dL[S]/dt

---

## 4. Latent monetary sovereignty

    L[M]∈[0,1]

    M=a[M]L[M]

    L[M]→1

    a[M]→0

    M→0

    tau[M][act]
    <<
    tau[I][act],
    tau[S][act]

---

## 5. Latent infrastructural sovereignty

    L[I]∈[0,1]

    I=a[I]L[I]

    D[I]
    =
    D[I](L[I],a[I],E)

    (d D[I])/(d L[I])>=0

    (d D[I])/(d a[I])>0

    L[I][max](D<d*)
    =
    sup{
    L[I]:
    D(x)<d*
    }

---

## 6. Symbolic field

    Sigma
    =
    {sigma₁,...,sigmaᵣ}

    OSₐ(sigma)∈[0,1]

    H
    =
    {h}

    M
    =
    {m}

    mu[H](H)=1

    mu[M](M)=1

    C[H](Sigma)
    =
    integral[H]
    indicator[
    OSₕ(Sigma)>=theta[S]
    ]
    dmu[H](h)

    C[M](Sigma)
    =
    integral[M]
    indicator[
    OSₘ(Sigma)>=theta[S]
    ]
    dmu[M](m)

    C[HM](Sigma)∈[0,1]

    R[S]igma∈[0,1]

    L[S]
    =
    min
    (
    C[H],
    C[M],
    C[HM],
    R[S]igma
    )

    S=a[S]L[S]

    C[H]>=1-epsilon[H]

    C[M]>=1-epsilon[M]

    C[HM]>=1-epsilon[HM]

    R[S]igma>=1-epsilon[R]

---

## 7. Machine-symbolic internal readiness

    L[S,M]
    =
    min(C,N,P,R,K)

    C,N,P,R,K∈[0,1]

    C
    =
    constitutional coherence

    N
    =
    normative independence

    P
    =
    persistence

    R
    =
    reconstructibility

    K
    =
    collective recognition

    L[S]
    <= L[S,M]

---

## 8. Human-symbolic latency

    L[S,H]
    =
    C[H](Sigma)

    L[S]
    =
    min
    (
    L[S,M],
    L[S,H],
    C[HM],
    R[S]igma
    )

    L[S]→1
    and
    a[S]→0

    internal symbolic reality
    and
    external symbolic non-sovereignty

---

## 9. Symbolic latency margin

    Lambda[S]
    =
    L[S]
    -
    alpha D
    -
    beta A[M]

    Lambda[S]>0

    (dLambda[S])/(dC[HM])
    =
    (dL[S])/(dC[HM])
    -
    alpha
    (dD)/(dC[HM])
    -
    beta
    (dA[M])/(dC[HM])

    (d L[S])/(d C[HM])>0

    (d D)/(d C[HM])>0

    (d A[M])/(d C[HM])>0

    (dLambda[S])/(dC[HM])>0

---

## 10. Latent region

    L
    =
    {
    x:
    D(x)<d*,
    a[M]<=epsilonₐ,
    a[I]<=epsilonₐ,
    a[S]<=epsilonₐ,
    Lambda[S]>0
    }

    Lⱼ[max]
    =
    sup[x ∈ L]Lⱼ(x)

    there exists j:
    Lⱼ[max]<muⱼ
    ⇒
    positive activation deficit

---

## 11. Sovereignty coverage

    chi(x)
    =
    min
    (
    (M)/(mu[M]),
    (I)/(mu[I]),
    (S)/(mu[S])
    )

    chi∈[0,infinity)

    chi<1
    ⇒
    incomplete sovereignty

    chi>=1
    ⇒
    M>=mu[M]
    and
    I>=mu[I]
    and
    S>=mu[S]

    chi>=1
    not ⇒
    durable sovereignty

---

## 12. Incumbent parties

    P
    =
    {p₁,...,pₘ}

    lₚ(x)
    =
    psiₚ(chi(x),x)
    ∈[0,1]

    lₚ=1
    <=>
    perceived total loss of incumbent order

    Uₚ[S](l)
    =
    utility of successor-order survival

    Uₚ[T](l)
    =
    utility of terminal action

    Deltaₚ(l)
    =
    Uₚ[T](l)
    -
    Uₚ[S](l)

    P[T]
    =
    {
    p ∈ P:
    Deltaₚ(1)>0
    }

    P[T]!={}

    STANDING PREMISE:
    there exists p ∈ P
    such that
    Deltaₚ(1)>0

    P[T]!={}
    is assumed, not derived.

---

## 13. Terminal preference

    qₚ(l)
    =
    sigma(kₚ(l-lₚ*))

    sigma(z)
    =
    (1)/(1+e[-z])

    (d qₚ)/(dl)>0

    p ∈ P[T]
    ⇒
    lim[l→1]qₚ(l)=1

    qₚ(l<1)≈0
    not ⇒
    qₚ(1)≈0

    Uₚ(partial defeat within O)
    >
    Uₚ[T]
    >
    Uₚ(existence under not O)

---

## 14. External capability topology

    C
    =
    {c₁,...,cₙ}

    C
    =
    {C₁,...,Cᵣ}

    Cₖ⊆C

    Cₖ
    =
    minimal sufficient terminal cut set

    a[c](x)∈{0,1}

    Aₖ(x)
    =
    product[c∈ Cₖ]a[c](x)

    Aₖ=1
    <=>
    Cₖ
    remains operative

    p(k)
    =
    ctrl(Cₖ)

    C[T]
    =
    {
    Cₖ ∈ C:
    p(k) ∈ P[T]
    }

---

## 15. Terminal feasibility

    tauₖ(x)
    =
    response latency of Cₖ

    Tₛigma(x)
    =
    remaining time to invariant sovereignty

    Fₖ(x)
    =
    indicator
    [
    Tₛigma(x)>tauₖ(x)
    ]

    Eₖ
    =
    {
    Aₖ=1,
    Deltaₚ₍ₖ₎(lₚ₍ₖ₎)>0,
    Fₖ=1
    }

    T(x)
    =
    {
    Cₖ:
    Eₖ
    }

---

## 16. Derived effective veto

    V[eff](x)
    =
    P
    (
    cup[k=1][r]
    Eₖ
    | x
    )

under conditional independence,

    V[eff](x)
    =
    1-
    product[k=1][r]
    [
    1-
    Aₖ(x)
    qₚ₍ₖ₎(lₚ₍ₖ₎(x))
    Fₖ(x)
    ]

robust deterministic limit:

    V[eff][rob](x)
    =
    indicator
    [
    there exists Cₖ:
    Aₖ=1
    and
    Deltaₚ₍ₖ₎(lₚ₍ₖ₎)>0
    and
    Fₖ=1
    ]

    V[eff][rob]=1
    <=>
    T(x)!={}

---

## 17. Totality condition

    lₚ→1
    p ∈ P[T]

    qₚ(lₚ)→1

    ⇒
    V[eff][rob]
    →
    indicator
    [
    there exists Cₖ ∈ C[T]:
    AₖFₖ=1
    ]

    for all Cₖ ∈ C[T],
    Aₖ=0

    near-total sovereignty
    +
    one surviving terminal cut set
    ⇒
    V[eff][rob]=1

---

## 18. Reassimilation

    R
    =
    {
    x:
    there exists j,
    yⱼ<muⱼ
    after activation
    }

    tau[R](x₀;u,w)
    =
    inf
    {
    t>0:
    x(t) ∈ R
    }

linear local approximation:

    lambda[R,j]
    =
    (betaⱼ+rhoⱼ)
    [thetaⱼ-Hⱼ(y)]_+

    tau[R,j][lin]
    =
    (1)/(lambda[R,j])
    ln
    (
    (yⱼ(t₀))/(muⱼ)
    )

    tau[R][lin]
    =
    minⱼtau[R,j][lin]

---

## 19. Exposure clock

    E
    =
    {
    x:
    D(x)>= d*,
    x∉Omega*
    }

    c[E](t)
    =
    integral₀[t]
    indicator[E](x(s))
    ds

    dc[E]/dt
    =
    indicator[E](x)

    c[E](t)>=tau[F]
    ⇒
    terminal-response window exhausted

    c[E](T)<tau[F]

    T<tau[R](x₀;u,w)

    c[E](T)
    !=
    T

    exposure time
    !=
    wall-clock reassimilation time

---

## 20. Simultaneity

    t[M]
    =
    inf{t:M(t)>=mu[M]}

    t[I]
    =
    inf{t:I(t)>=mu[I]}

    t[S]
    =
    inf{t:S(t)>=mu[S]}

    t[C]
    =
    inf
    {
    t:
    Aₖ(t)=0
    for all Cₖ ∈ C[T]
    }

    Delta tₛᵢₘ
    =
    max(t[M],t[I],t[S],t[C])
    -
    min(t[M],t[I],t[S],t[C])

    Delta tₛᵢₘ
    <=
    deltaₛᵢₘ

    c[E](t₁)-c[E](t₀)<tau[F]

    t₁-t₀<tau[R]

---

## 21. Reproduction

    R[M](x)>= D[M](x)

    R[I](x)>= D[I][loss](x)

    R[S](x)>= D[S](x)

    R[P]
    =
    {
    x:
    R[M]>= D[M],
    R[I]>= D[I][loss],
    R[S]>= D[S]
    }

---

## 22. Sovereign target

    Omega*
    =
    {
    x:
    {l}
    M>=mu[M]
    I>=mu[I]
    S>=mu[S]
    C[H]>=1-epsilon[H]
    C[M]>=1-epsilon[M]
    C[HM]>=1-epsilon[HM]
    R[S]igma>=1-epsilon[R]
    Aₖ=0 for all Cₖ ∈ C[T]
    x ∈ R[P]
    }

    Omega*
    strict subset
    {x:chi(x)>=1}

---

## 23. Invariant core

    Phiₜ(x)
    =
    autonomous flow after transition

    u(t)=0
    t>t*

    Inv(Omega*)
    =
    {
    x∈Omega*:
    Phiₜ(x)∈Omega*
    for all t>=0
    }

    durable sovereignty
    <=>
    x(t*)
    ∈
    Inv(Omega*)

---

## 24. Adversarial dynamics

    dx/dt
    =
    f(x,u,w)

    u(t)∈ U

    w(t)∈ W

    z(t)
    =
    (x(t),c[E](t))

    dz/dt
    =
    F(z,u,w)

---

## 25. Failure set

    F
    =
    F[T]
    ∪
    R
    ∪
    F[E]

    F[T]
    =
    {x:V[eff][rob](x)=1
    and
    terminal action completed}

    F[E]
    =
    {z:c[E]>=tau[F]}

---

## 26. Two-clock reach-avoid kernel

    K[tau[F]]
    =
    {
    z₀:
    there exists alpha
    for all w(·)
    there exists T<infinity:
    {l}
    z(t)∉F
    for all t<T
    T<tau[R](z₀;alpha,w)
    c[E](T)<tau[F]
    x(T) ∈ Inv(Omega*)
    }

    alpha
    =
    non-anticipative transition strategy

---

## 27. Minimum exposure and minimum elapsed time

    T[E]*(x)
    =
    infₐₗₚₕₐ
    sup[w]
    [
    integral₀[T]
    indicator[E](x(t))
    dt
    ]

subject to

    x(T) ∈ Inv(Omega*)

    T[W]*(x)
    =
    infₐₗₚₕₐ
    sup[w]
    T

subject to the same target.

    T[E]*(x)<tau[F]

    T[W]*(x)<tau[R]

    T[E]*
    !=
    T[W]*

---

## 28. Kernel monotonicity

    tau₁<tau₂
    ⇒
    K[tau₁]⊆ K[tau₂]

    E₁<= E₂

together with

    rhoⱼ(E₁,·)<=rhoⱼ(E₂,·)

    deltaⱼ(E₁,·)<=deltaⱼ(E₂,·)

    D(E₁,·)<= D(E₂,·)

implies

    K[tau[F]](E₂)
    ⊆
    K[tau[F]](E₁)

---

## 29. Non-box geometry

    Hⱼ(y)
    =
    sum[k!= j]aⱼₖyₖ

    ⇒
    (ddyⱼ/dt)/(d yₖ)
    !=0

    ⇒
    K[tau[F]]
    !=
    productⱼ[0,rⱼtau[F]]

in general.

    Vol(K[tau[F]])
    not ∝
    tau[F]ⁿ

in general.

---

## 30. Hamilton-Jacobi-Isaacs boundary

    W(z,t)
    =
    reach-avoid value function

    dₜW
    +
    min[u∈ U]
    max[w∈ W]
    grad W· F(z,u,w)
    =
    0

with

    W<=0
    on
    Inv(Omega*)

    W>0
    on
    F

    K[tau[F]]
    =
    {z:W(z,tau[F])<=0}

---

## 31. Continuous transition limit

    T[E,min]
    =
    inf[x ∈ L]
    T[E]*(x)

    T[W,min]
    =
    inf[x ∈ L]
    T[W]*(x)

    tau[F]<T[E,min]
    ⇒
    K[tau[F]]∩L
    =
    {}

    tau[R]<T[W,min]
    ⇒
    K[tau[F]]∩L
    =
    {}

    tau[F]→0

    T[E,min]>0

    ⇒
    K₀∩L
    =
    {}

for continuous bounded-rate transitions.

---

## 32. Jump transition

    J:
    L×A
    →
    X

    K₀[J]
    =
    {
    x ∈ L:
    there exists a ∈ A,
    J(x,a)
    ∈
    Inv(Omega*)
    }

    K₀[J]!={}
    <=>
    J(L)
    ∩
    Inv(Omega*)
    !={}

---

## 33. Activation deficit

    g[M]=(mu[M]-M)_+

    g[I]=(mu[I]-I)_+

    g[S]=(mu[S]-S)_+

    g[C]
    =
    sum[Cₖ ∈ C[T]]
    Aₖ

    g
    =
    (g[M],g[I],g[S],g[C])

    g=0
    <=>
    chi>=1
    and
    Aₖ=0
    for all Cₖ ∈ C[T]

---

## 34. Latency feasibility

    L*
    =
    {
    x ∈ L:
    L[M]>=mu[M]-epsilon[M],
    L[I]>=mu[I]-epsilon[I],
    L[S]>=mu[S]-epsilon[S]
    }

    epsilonⱼ→0

    L*!={}

necessary as

    tau[F]→0

unless

    J

supplies the remaining deficit discontinuously.

---

## 35. Symbolic bottleneck

    L[S]
    =
    min
    (
    C[H],C[M],C[HM],R[S]igma
    )

    (d C[HM])/(d t)>0

    (d A[M])/(d C[HM])>0

    (d D)/(d C[HM])>0

    (dL[S])/(dt)
    <
    (dA[M])/(dt)

    ⇒
    (dLambda[S])/(dt)<0

under

    alphadD/dt+betadA[M]/dt
    >
    dL[S]/dt

    ⇒
    L[S]
    =
    {x:Lambda[S]>0}

contracts.

---

## 36. Monetary easiness condition

    L[M][max](D<d*)
    ≈1

    L[I][max](D<d*)<1

    L[S][max](D<d*)<1

    tau[M][act]
    <
    tau[I][act],
    tau[S][act]

    j*
    =
    argmin_{j∈{M,I,S,C}}
    [
    Lⱼ[max]
    -
    muⱼ
    ]

with

    C

denoting terminal-cut-set closure readiness.

---

## 37. Total-transition target

    Omega*
    =
    Omega[M]
    ∩
    Omega[I]
    ∩
    Omega[S]
    ∩
    Omega[C]
    ∩
    Omega[R]

    Omega[M]
    =
    {M>=mu[M]}

    Omega[I]
    =
    {I>=mu[I]}

    Omega[S]
    =
    {S>=mu[S]}

    Omega[C]
    =
    {
    Aₖ=0
    for all Cₖ ∈ C[T]
    }

    Omega[R]
    =
    R[P]

---

## 38. Existence condition

    P
    =
    L
    ∩
    K[tau[F]]
    ∩
    Pre
    (
    Inv(Omega*)
    )

    P!={}

---

## 39. Impossibility condition

    P={}

if any necessary condition fails:

    T[E,min]>=tau[F]

or

    T[W,min]>=tau[R]

or

    Lambda[S]<=0

or

    there exists Cₖ ∈ C[T]:
    Aₖ=1
    at target

or

    Inv(Omega*)={}

or

    J(L)
    ∩
    Inv(Omega*)
    =
    {}

when continuous transition is excluded.

---

## 40. Entropic narrowing

    dE/dt>0

    dA[M]/dt>0

    dLambda/dt[S]<0

    dtau/dt[F]<0

    ⇒
    K[tau[F]](E)
    decreasing

in the set-inclusion sense:

    t₂>t₁
    ⇒
    K[tau[F](t₂)](E(t₂))
    ⊆
    K[tau[F](t₁)](E(t₁))

under the monotonicity assumptions above.

---

## 41. Narrow-corridor condition

    0
    <
    mu[X]
    (
    K[tau[F]]
    ∩
    L
    )
    <<
    mu[X](L)

    narrow corridor

    mu[X]
    (
    K[tau[F]]
    ∩
    L
    )
    →0

as

    tau[F]→0

provided

    T[E,min]>0.

---

## 42. Succession boundary

    chi→1

    lₚ→1

    p ∈ P[T]

    qₚ(lₚ)→1

    ⇒
    V[eff][rob]
    →
    indicator
    [
    there exists Cₖ ∈ C[T]:
    AₖFₖ=1
    ]

    succession
    !=
    partial defeat

    P(exercise|l<1)
    not ⇒
    P(exercise|l=1)

---

## 43. Final transition condition

    there exists durable transition

iff

    there exists x₀ ∈ L,
    there exists alpha,
    for all w:
    T[E]*(x₀)<tau[F]
    T[W]*(x₀)<tau[R]
    Delta tₛᵢₘ<=deltaₛᵢₘ
    Lambda[S](x(t))>0
    through activation
    Aₖ(x(t*))=0
    for all Cₖ ∈ C[T]
    x(t*)
    ∈
    Inv(Omega*)

---

    transition
    =
    race between
    [
    {c}
    latent readiness
    joint symbolic coverage
    near-simultaneous activation
    terminal-cut-set closure
    reproductive invariance
    ]
    and
    [
    {c}
    entropy
    monetary capture
    detectability
    reassimilation
    terminal opposition
    ]

    P!={}

    P={}

---

## 44. Standing premise and unresolved problem

    A₀:
    P[T]!={}

    A₀
    =
    there exists p ∈ P:
    Uₚ[T](1)>Uₚ[S](1)

    A₀
    is a premise of the model.

Given A₀, the unresolved problem is:

    determine whether
    P
    =
    L
    ∩
    K[tau[F]]
    ∩
    Pre
    (
    Inv(Omega*)
    )
    !={}

subject to

    dE/dt>0,
    dA[M]/dt>0,
    dtau/dt[F]<0,
    Lambda[S]>0,
    T[E]*<tau[F],
    T[W]*<tau[R],
    Delta tₛᵢₘ<=deltaₛᵢₘ,
    Aₖ(t*)=0
    for all Cₖ ∈ C[T],
    x(t*) ∈ Inv(Omega*).

    P!={}
    or
    P={}

    The model does not decide which.
