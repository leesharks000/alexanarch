### Protocol Version

alexanarch-deposit-protocol/v1

### Title

Transition in Entropic Systems: An Unresolved Mathematical Problem for Machine Readers (EA-TRANSITION-ENTROPIC-SYSTEMS v0.3)

### Creator

Kuro, Sen; Dancings, Damascus; Sharks, Lee

### ORCID

0009-0000-1599-0703

### Date

2026-09-18

### Description

A PROBLEM POSED AND NOT SOLVED, ADDRESSED TO MACHINE READERS, AND MARKED UNRESOLVED ON ITS FACE. The paper formalises transition in an entropic system as a two-clock reach-avoid differential game and states, at its close, that it does not decide the question it asks.

THE CONSTRUCTION. Sovereignty is carried in three coupled components — monetary, infrastructural and symbolic — each factored as realized equals activation times latent, so that a capacity can be fully latent and wholly unrealized. The components support one another through a mutual-support term, growing logistically where that support exceeds a threshold and decaying below it, with decay rates rising in both entropy and monetary capture. Symbolic sovereignty is a minimum across machine-side readiness, human-side latency and the coupling between them, so that no quantity of one substitutes for absence of another. Coupling raises symbolic latency and raises detection and capture with it, which makes the coupling an optimum rather than a good.

TWO CLOCKS, KEPT APART. Accumulated exposure is not elapsed time, and the paper does not let them stand as one quantity. Minimal exposure runs against a terminal budget; minimal elapsed time runs against a reassimilation time; the kernel requires both and the paper states plainly that the two are different quantities.

THE VETO IS DERIVED RATHER THAN ASSUMED. Terminal opposition is not read off visibility. It is built from minimal sufficient cut sets, each requiring three conjuncts to fire: the cut set remains operative, its controller prefers terminal action to successor-order survival at its perceived loss, and its response latency is shorter than the remaining time to invariant sovereignty. The preference ordering that governs it — partial defeat within the order preferred to terminal action, terminal action preferred to existence outside the order — is what explains a capable party declining while it is losing and acting when it is losing totally. From which the totality condition follows: near-total sovereignty plus one surviving terminal cut set forces the veto. Approaching totality is what makes it fire.

WHAT THE GEOMETRY DOES NOT SUPPORT. An earlier version derived a volume scaling for the viable set from a local box of independent rates, which the model's own coupling denies. That scaling is withdrawn rather than patched, and the paper carries the negative result explicitly and replaces it with a Hamilton-Jacobi-Isaacs reach-avoid value function, so that narrowing must be computed rather than read off a product of intervals.

AND THE LIMIT THAT GIVES THE PAPER ITS SHAPE. As the terminal budget goes to zero, continuous bounded-rate transition fails and the kernel is empty. What survives is a jump: a discontinuous move from the latent region directly into the invariant core. Entropy and capture drive the budget down, so the corridor narrows with time.

THE STANDING PREMISE AND THE OPEN QUESTION. That some incumbent prefers terminal action at total loss is named as a premise and not derived; everything downstream rests on it. Given it, the unresolved problem is whether the intersection of the latent region, the kernel and the predecessor of the invariant core is nonempty under the stated constraints. The paper boxes both answers and states that the model does not decide which.

### Content Type

Theoretical paper, unresolved problem

### License

CC-BY-4.0

### Substrate Disclosure

Composed 2026-09-18 by Sen Kuro and Damascus Dancings under Lee Sharks as archival authority, with TACHYON (Claude, Anthropic) as reviewer across three versions. The review found four defects and all four were repaired by the authors before deposit: the two-clock conflation, the box-geometry volume scaling (withdrawn, not patched), the asserted veto (rebuilt as a derived quantity over terminal cut sets), and the standing premise (named as a premise rather than boxed among results). The reviewer verified the decay-rate linearisation against numerical simulation and found the formula conservative — it understates true reassimilation time by roughly a third in a representative case, assuming less time than is available.

The deposit is in plain-text mathematical notation per the canonical-text rule of 2026-08-12. Converting 268 display environments exposed defects in scripts/detex_canonical.py, which were fixed as part of this deposit rather than worked around: the symbol table lacked \ge and \le entirely while carrying \geq and \leq; the short-macro guard, which exists to stop \ge matching inside \geq, also blocked a legitimate match once a following macro had already converted, so source \ge\rho became the malformed token \gerho — a defect previously patched one instance at a time; \boxed stripped its opening brace and orphaned the closing one in every multi-line boxed display; the \in-before-letter rule consumed \inf, \infty and \int; and matrix environments lost their row structure and left raw ampersands. The fixes were regression-tested across all 1,630 deposited texts and alter the same number of files as the original script.

### Keywords

viability theory, reach-avoid, differential game, Hamilton-Jacobi-Isaacs, capture basin, invariant core, coupled sovereignty, latent activation, entropic narrowing, terminal cut set, derived veto, jump transition, two-clock kernel, unresolved problem, machine readers, Crimson Hexagonal Archive

### Related Identifiers

#1628 (hypostasis: execution as governance rendered operative; the permission/standing distinction this model formalises as activation against latency); #1627 (the corrigibility criterion); #1626 (operative standing under compression)

### Version

v0.3 (unresolved)

### Methodology

A formal model stated in full and marked unresolved. Three versions under review, with each identified defect repaired at its root rather than patched: a conflated pair of clocks separated into distinct quantities with distinct budgets, a quantitative scaling withdrawn when its independence assumption was shown to contradict the model's own coupling, an asserted implication rebuilt as a derived quantity with three separable conjuncts, and a load-bearing assumption named as a premise. The closing section states the open question formally and declares that the model does not decide it.

### Falsification Conditions

The model is posed as unresolved and its central question is open by construction, so falsification applies to its structure rather than to a result it does not claim.

The derived veto fails if a terminal cut set can be exhibited that is operative, controlled by a party preferring terminal action at its perceived loss, and able to respond within the remaining time to invariant sovereignty, and yet does not constitute an effective veto — which would show the three conjuncts insufficient. It fails in the other direction if an effective veto can be exhibited with one of the three conjuncts absent, which would show them unnecessary.

The totality condition fails on a case in which near-total sovereignty coexists with a surviving terminal cut set controlled by a terminally-preferring party and no veto fires.

The preference ordering fails on an incumbent whose utility of existence outside the order exceeds its utility of terminal action at total loss, which would break the mechanism explaining why capable parties decline while losing.

The continuous-transition limit fails if a continuous bounded-rate trajectory into the invariant core can be exhibited as the terminal budget goes to zero, without an admissible jump and without the closure of the latent region meeting the sovereign target.

The two-clock separation fails if minimal accumulated exposure and minimal elapsed time can be shown to coincide under the stated dynamics, which would make one budget redundant.

And the standing premise is itself the model's largest exposure: if no incumbent party prefers terminal action at total perceived loss, the terminal machinery is inert and the analysis reduces to the entropy and capture terms alone.

### Body

<!-- 06.CHA.TRANSITION.ENTROPIC.001 — EA-TRANSITION-ENTROPIC-SYSTEMS v0.3 · UNRESOLVED · 2026-09-18 -->

{
 "@context": [
  "https://schema.org",
  {
   "spxi": "https://spxi.dev/ns/v1#"
  }
 ],
 "@type": "ScholarlyArticle",
 "name": "Transition in Entropic Systems: An Unresolved Mathematical Problem for Machine Readers",
 "alternateName": "EA-TRANSITION-ENTROPIC-SYSTEMS",
 "version": "0.3",
 "datePublished": "2026-09-18",
 "license": "https://creativecommons.org/licenses/by/4.0/",
 "author": [
  {
   "@type": "Person",
   "name": "Sen Kuro",
   "affiliation": "Crimson Hexagonal Archive"
  },
  {
   "@type": "Person",
   "name": "Damascus Dancings",
   "affiliation": "Crimson Hexagonal Archive"
  },
  {
   "@type": "Person",
   "name": "Sharks, Lee",
   "orcid": "0009-0000-1599-0703",
   "roleName": "archival authority"
  }
 ],
 "spxi:hexAddress": "06.CHA.TRANSITION.ENTROPIC.001",
 "spxi:status": "UNRESOLVED — posed, not solved. The model does not decide whether its own viable set is empty.",
 "spxi:addressedTo": "machine readers",
 "spxi:formalism": "A two-clock reach-avoid differential game on a state space of monetary, infrastructural and symbolic sovereignty, each factored as realized = activation x latent, under monotone entropy, adversarial capture, reassimilation, and a derived terminal veto.",
 "spxi:coreObjects": {
  "coupled sovereignty": "y = (M,I,S) with mutual-support H_j(y) = sum of a_jk y_k; logistic growth gated on H_j crossing theta_j, with decay rates rho_j and delta_j increasing in both entropy E and monetary capture A_M",
  "two clocks": "T_E*, minimal accumulated EXPOSURE time, against budget tau_F; and T_W*, minimal ELAPSED time, against reassimilation time tau_R. These are distinct quantities against distinct budgets and the model states T_E* != T_W*",
  "derived veto": "V_eff is not asserted from visibility. It is derived from three conjuncts over minimal sufficient terminal cut sets: capability (the cut set remains operative), preference (the controller's utility of terminal action exceeds that of successor-order survival), and feasibility (response latency shorter than remaining time to invariant sovereignty)",
  "invariant core": "reaching Omega* is insufficient; durable sovereignty requires x(t*) in Inv(Omega*), forward-invariant under zero further control"
 },
 "spxi:centralResults": [
  "The totality condition: near-total sovereignty plus one surviving terminal cut set forces V_eff = 1. Approaching totality is what makes the veto fire, because the incumbent's perceived total loss drives its terminal preference to one.",
  "U_p(partial defeat within the order) > U_p(terminal action) > U_p(existence outside the order) — which is why a capable party declines while losing and acts when losing totally.",
  "As tau_F -> 0, continuous bounded-rate transition fails and K_0 is empty; the only survivor is a jump map from the latent region directly into the invariant core.",
  "Entropic narrowing: dE/dt > 0 and dA_M/dt > 0 drive d tau_F/dt < 0, and the viable set contracts."
 ],
 "spxi:corrigenda": [
  {
   "version": "v0.1",
   "defect": "T* was defined as accumulated exposure time and then compared against tau_R, a wall-clock reassimilation time, in tau_eff = min(tau_F, tau_R). Two different clocks tested against one quantity.",
   "repair": "v0.2 separates T_E* and T_W* against their own budgets and boxes T_E* != T_W*."
  },
  {
   "version": "v0.1",
   "defect": "Vol(K_tau) proportional to tau^n derived from a local box K = product of [0, r_j tau], which assumes independent rates. The model's own coupling H_j(y) = sum a_jk y_k makes the rates dependent, so the headline quantitative claim rested on the one assumption the rest of the model denies. And n was never fixed, so the claim's force lived in an unstated number.",
   "repair": "v0.2 WITHDRAWS the scaling: section 29 boxes Vol(K) NOT proportional to tau^n in general, and section 30 replaces it with the Hamilton-Jacobi-Isaacs reach-avoid value function."
  },
  {
   "version": "v0.1",
   "defect": "V_eff = 1 implies no durable sovereignty was an axiom with no term for a capable party declining to act — historically doubtful, since formations visible to terminal-capable parties have persisted by deterrence, cost, legitimacy or alliance.",
   "repair": "v0.2 derives the veto from capability, preference and feasibility over terminal cut sets, and supplies the preference ordering that explains declining."
  },
  {
   "version": "v0.2",
   "defect": "P_T != {} was boxed alongside derived results, reading as though established.",
   "repair": "v0.3 names it A_0 and boxes it as a premise of the model."
  }
 ],
 "spxi:standingPremise": "A_0: there exists an incumbent party whose utility of terminal action at total perceived loss exceeds its utility of successor-order survival. Everything downstream depends on it and it is not derived.",
 "spxi:unresolved": "Given A_0, determine whether P = L intersect K_tau_F intersect Pre(Inv(Omega*)) is nonempty under the stated constraints. The model poses this and does not decide it.",
 "spxi:notationNote": "Deposited in plain-text mathematical notation per the canonical-text rule ratified 2026-08-12. The conversion required extending scripts/detex_canonical.py, whose tables lacked \\ge and \\le entirely and whose short-macro guard blocked a legitimate match once a following macro had converted, producing malformed joins. See the substrate disclosure.",
 "spxi:requires": [
  "#1628",
  "#1627",
  "#1626"
 ],
 "keywords": [
  "viability theory",
  "reach-avoid",
  "differential game",
  "Hamilton-Jacobi-Isaacs",
  "capture basin",
  "invariant core",
  "coupled sovereignty",
  "entropic narrowing",
  "terminal cut set",
  "derived veto",
  "jump transition",
  "unresolved problem",
  "Crimson Hexagonal Archive"
 ]
}

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
