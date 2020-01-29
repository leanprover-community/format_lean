-- begin header

-- Everything in the header will be hidden in the HTML file.
import data.real.basic

notation `|` x `|` := abs x

@[user_attribute]
meta def ineq_rules : user_attribute :=
{ name := `ineq_rules,
  descr := "lemmas usable to prove inequalities" }

attribute [ineq_rules] add_lt_add le_max_left le_max_right

meta def obvious_ineq := `[linarith <|> apply_rules ineq_rules]
run_cmd add_interactive [`obvious_ineq]
-- end header

/-
# The sandwich theorem

In this demo file, we define limits of sequences of real numbers and prove the sandwich theorem.
-/

/- Definition
A sequence of real numbers $a_n$ tends to $l$ if
$\forall \varepsilon > 0, \exists N, \forall n \geq N, |a_n - l | \leq \varepsilon$.
-/
definition is_limit (a : ℕ → ℝ) (l : ℝ) :=
∀ ε > 0, ∃ N, ∀ n ≥ N, | a n - l | < ε

/- Theorem
If $(a_n)$, $(b_n)$, and $(c_n)$ are three real-valued sequences satisfying $a_n ≤ b_n ≤ c_n$ for all $n$, and if furthermore $a_n→ℓ$ and $c_n→ℓ$, then $b_n→ℓ$.
-/
theorem sandwich (a b c : ℕ → ℝ)
  (l : ℝ) (ha : is_limit a l) (hc : is_limit c l) 
  (hab : ∀ n, a n ≤ b n) (hbc : ∀ n, b n ≤ c n) : is_limit b l :=
begin
  -- We need to show that for all $ε>0$ there exists $N$ such that $n≥N$ implies $|b_n-ℓ|<ε$. So choose ε > 0.
  intros ε Hε,
  -- we now need an $N$. As usual it is the max of two other N's, one coming from $(a_n)$ and one from $(c_n)$. Choose $N_a$ and $N_c$ such that $|aₙ - l| < ε$ for $n ≥ Na$ and $|cₙ - l| < ε$ for $n ≥ Nc$.
  cases ha ε Hε with Na Ha,
  cases hc ε Hε with Nc Hc,
  -- Now let $N$ be the max of $N_a$ and $N_c$; we claim that this works.
  let N := max Na Nc,
  use N,
  -- Note that $N ≥ N_a$ and $N ≥ N_c$,
  have HNa : Na ≤ N := by obvious_ineq,  
  have HNc : Nc ≤ N := by obvious_ineq,
  -- so for all n ≥ N, 
  intros n Hn,
  -- we have $n≥ N_a$ and $n\geq N_c$, so $aₙ ≤ bₙ ≤ cₙ$, and $|aₙ - l|, |bₙ - l|$ are both less than $\epsilon$.
  have h1 : a n ≤ b n := hab n,
  have h2 : b n ≤ c n := hbc n,
  have h3 : |a n - l| < ε := Ha n (le_trans HNa Hn),
  have h4 : |c n - l| < ε := Hc n (le_trans HNc Hn),
  -- The result now follows easily from these inequalities (as $l-ε<a_n≤b_n≤c_n<l+ε$). 
  revert h3,revert h4,
  unfold abs,unfold max,
  split_ifs;intros;linarith,
end
