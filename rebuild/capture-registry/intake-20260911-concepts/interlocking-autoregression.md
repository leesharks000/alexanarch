**USER:** "interlocking autoregression"

**GOOGLE AI MODE:**
In statistics and econometrics, interlocking autoregression refers to a system of
multiple, mutually dependent autoregressive equations where the variables influence
each other across time. Instead of a single variable being predicted solely by its own
past (a univariate autoregressive model), multiple variables are bound together in a
network of feedback loops. [1, 2]
The most prominent and widely recognized implementation of this concept is the Vector
Autoregressive (VAR) model. [1]

How "Interlocking" Dynamics Work
In a standard autoregressive (AR) model, you predict \(Y_{t}\) using past values of Y
(e.g., \(Y_{t-1}, Y_{t-2}\)). [1]
In an interlocking (multivariate) system like a VAR(1) model, you have two or more
variables—let's say Consumer Spending (C) and Personal Income (I). They "interlock"
because spending depends on past income, and income simultaneously depends
on past spending: [1]
\(C_{t}=\alpha _{1}+\beta _{11}C_{t-1}+\beta _{12}I_{t-1}+\epsilon _{1,t}\)
\(I_{t}=\alpha _{2}+\beta _{21}C_{t-1}+\beta _{22}I_{t-1}+\epsilon _{2,t}\)
Because every variable is treated symmetrically as an endogenous variable that affects
every other variable in the system over time, the stochastic difference equations are
tightly intertwined. [1]

Core Variations of Interlocking Autoregression
Model Type

Dynamic Nature

Best Used For...

Vector Autoregression (VAR)

Linear, interlocking equations
across stable time series.

Macroeconomic forecasting
(e.g., inflation vs. interest
rates).

Space-Time Autoregression
(STAR)

Interlocking over both temporal
lags and geographic neighbor
data.

Real estate pricing or
epidemiology (disease spread
across regions).

Nonlinear / Compartmental
AR

Coupled, non-linear mass or
density transfers between
nodes.

Ecosystem modeling,
supply-chain flow, or
population dynamics.

Why Use an Interlocking System?
1.​ Captures Feedback Loops: It models complex real-world systems where cause
and effect are bidirectional over time.
2.​ No Need for Strict Structural Assumptions: Unlike traditional structural
models, you don't have to specify which variable is strictly the "cause" and which
is the "effect"—the data reveals the relationships. [1]

To help unpack this concept for your specific needs, could you share:
●​ Are you looking at this from a macroeconomic, machine learning, or spatial
data standpoint?
●​ Do you need help setting up equations, or are you looking to write the code to
implement a model?

Wikipedia

Autoregressive model - Wikipedia
Together with the moving-average (MA) model, it is a special case and key component of the more general
autoregressive–moving-average (ARMA) and autoregressive ...

OpenText

Autoregression algorithms | Vertica 24.2.x
AR is a univariate autoregressive time series algorithm that predicts a variable's future values based on its preceding
values. The user specifies the number of...

Levi John Wolf

Autoregressive Stochastic Processes
These were suggested first by Cliff & Ord in early work, extended by Pfeifer & Deutsch (1980), see a very rigorous
treatment in RJ Bennett's book and are also d...

YouTube·edureka!

8:47

Autoregressive Models | Auto Regression | Machine Learning for Beginners | Edureka

Stack Exchange

Nonlinear Autoregressive model parameter estimation from time series
Jan 26, 2015 — I'm working on a nonlinear multivariate autoregressive model of order 1 (markovian). It is a discrete-time
dynamical system which models exchange of mass betwee...