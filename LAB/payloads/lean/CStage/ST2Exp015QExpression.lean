/- Adapted proof pattern; see ST2-EXP-015_IMPLEMENTATION_PROVENANCE_001.md. -/
/- ST2-EXP-015 Route Q: noncanonical quadratic-expression quotient probe.

This is a formal-expression / normalization / quotient-style adjunction
candidate. It is not a claim that a full polynomial ring R[X] has already
been constructed. All coefficient-normal-form declarations are local to this
namespace; the source does not import the Route P probe.
-/
namespace BOMA.C.StageTwo.QExpression015

open BOMA.R.StageTwo.CauchyQuotient003
open BOMA.R.StageTwo.CauchyAdditive003
open BOMA.R.StageTwo.CauchyMultiplicative003
open BOMA.R.StageTwo.CauchyOrderCore003
open BOMA.C.StageTwo.ScalarInterface015

open BOMA.C.StageTwo.ScalarConsequences015

/-- Route-Q-local quadratic normal form; independent of Route P declarations. -/
structure NormalForm where
  re : RCBOMA
  im : RCBOMA

/-- Core Lean does not supply a generated structure-extensionality lemma. -/
theorem normal_ext {u v : NormalForm}
    (hre : u.re = v.re) (him : u.im = v.im) :
    u = v := by
  cases u
  cases v
  cases hre
  cases him
  rfl

def nfReal (a : RCBOMA) : NormalForm := ⟨a, rCZero⟩
def nfImag : NormalForm := ⟨rCZero, rCOne⟩

def nfNeg (u : NormalForm) : NormalForm :=
  ⟨rCNeg u.re, rCNeg u.im⟩

def nfAdd (u v : NormalForm) : NormalForm :=
  ⟨rCAdd u.re v.re, rCAdd u.im v.im⟩

def nfMul (u v : NormalForm) : NormalForm :=
  ⟨rCAdd (rCMul u.re v.re)
      (rCNeg (rCMul u.im v.im)),
   rCAdd (rCMul u.re v.im)
      (rCMul u.im v.re)⟩

/-- Freely written finite quadratic-adjunction expressions. -/
inductive Expr where
  | coeff : RCBOMA → Expr
  | generator : Expr
  | neg : Expr → Expr
  | add : Expr → Expr → Expr
  | mul : Expr → Expr → Expr

/-- Evaluation modulo the declared generator relation X² = -1. -/
def normalize : Expr → NormalForm
  | .coeff a => nfReal a
  | .generator => nfImag
  | .neg e => nfNeg (normalize e)
  | .add e f => nfAdd (normalize e) (normalize f)
  | .mul e f => nfMul (normalize e) (normalize f)

def exprEquiv (e f : Expr) : Prop := normalize e = normalize f

def exprSetoid : Setoid Expr where
  r := exprEquiv
  iseqv :=
    ⟨(fun _ => rfl),
      (fun h => h.symm),
      (fun h₁ h₂ => h₁.trans h₂)⟩

/-- Route-Q carrier: syntax modulo equal quadratic normal forms. -/
def QuotientCandidate : Type := Quotient exprSetoid

def qmk (e : Expr) : QuotientCandidate :=
  Quotient.mk exprSetoid e

theorem qmk_eq_iff {e f : Expr} :
    qmk e = qmk f ↔ normalize e = normalize f := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

theorem neg_respects {e e' : Expr}
    (h : exprEquiv e e') :
    exprEquiv (.neg e) (.neg e') := by
  change nfNeg (normalize e) = nfNeg (normalize e')
  rw [h]

theorem add_respects {e e' f f' : Expr}
    (he : exprEquiv e e')
    (hf : exprEquiv f f') :
    exprEquiv (.add e f) (.add e' f') := by
  change nfAdd (normalize e) (normalize f) =
    nfAdd (normalize e') (normalize f')
  rw [he, hf]

theorem mul_respects {e e' f f' : Expr}
    (he : exprEquiv e e')
    (hf : exprEquiv f f') :
    exprEquiv (.mul e f) (.mul e' f') := by
  change nfMul (normalize e) (normalize f) =
    nfMul (normalize e') (normalize f')
  rw [he, hf]

def neg : QuotientCandidate → QuotientCandidate :=
  Quotient.lift
    (fun e => qmk (.neg e))
    (fun _ _ h => Quotient.sound (neg_respects h))

def add : QuotientCandidate → QuotientCandidate → QuotientCandidate :=
  Quotient.lift₂
    (fun e f => qmk (.add e f))
    (fun _ _ _ _ he hf => Quotient.sound (add_respects he hf))

def mul : QuotientCandidate → QuotientCandidate → QuotientCandidate :=
  Quotient.lift₂
    (fun e f => qmk (.mul e f))
    (fun _ _ _ _ he hf => Quotient.sound (mul_respects he hf))

def ofR (a : RCBOMA) : QuotientCandidate := qmk (.coeff a)
def zero : QuotientCandidate := ofR rCZero
def one : QuotientCandidate := ofR rCOne
def imag : QuotientCandidate := qmk .generator

theorem add_zero_right_from_interface
    (C : CauchyScalarCertificate) (x : RCBOMA) :
    rCAdd x rCZero = x := by
  calc
    rCAdd x rCZero = rCAdd rCZero x := C.addComm x rCZero
    _ = x := C.addZeroLeft x

theorem mul_one_right_from_interface
    (C : CauchyScalarCertificate) (x : RCBOMA) :
    rCMul x rCOne = x := by
  calc
    rCMul x rCOne = rCMul rCOne x := C.mulComm x rCOne
    _ = x := C.mulOneLeft x

/-- P/Q-03: quotient identity preserves faithful real coefficients. -/
theorem ofR_injective {a b : RCBOMA}
    (h : ofR a = ofR b) : a = b := by
  have hn : normalize (.coeff a) = normalize (.coeff b) :=
    (qmk_eq_iff.mp h)
  exact congrArg NormalForm.re hn

/-- Route-local normal form of a formal real-plus-imaginary expression. -/
theorem normalized_coordinate_expression
    (C : CauchyScalarCertificate) (a b : RCBOMA) :
    normalize (.add (.coeff a) (.mul (.coeff b) .generator)) =
      ⟨a, b⟩ := by
  apply normal_ext
  · change
      rCAdd a
        (rCAdd (rCMul b rCZero)
          (rCNeg (rCMul rCZero rCOne))) = a
    rw [mul_zero_right_from_interface C b,
        mul_zero_left_from_interface C rCOne,
        neg_zero_from_interface C,
        C.addZeroLeft rCZero,
        add_zero_right_from_interface C a]
  · change
      rCAdd rCZero
        (rCAdd (rCMul b rCOne)
          (rCMul rCZero rCZero)) = b
    rw [mul_one_right_from_interface C b,
        mul_zero_left_from_interface C rCZero,
        add_zero_right_from_interface C b,
        C.addZeroLeft b]

/-- P/Q-06: quotient identity enforces the declared quadratic relation. -/
theorem imag_squared
    (C : CauchyScalarCertificate) :
    mul imag imag = neg one := by
  apply Quotient.sound
  change nfMul nfImag nfImag = nfNeg (nfReal rCOne)
  apply normal_ext
  · change
      rCAdd (rCMul rCZero rCZero)
        (rCNeg (rCMul rCOne rCOne)) = rCNeg rCOne
    rw [mul_zero_left_from_interface C rCZero,
        C.mulOneLeft rCOne,
        C.addZeroLeft (rCNeg rCOne)]
  · change
      rCAdd (rCMul rCZero rCOne)
        (rCMul rCOne rCZero) = rCNeg rCZero
    rw [mul_zero_left_from_interface C rCOne,
        C.mulOneLeft rCZero,
        C.addZeroLeft rCZero,
        neg_zero_from_interface C]

/-- Every raw expression is equivalent to its declared quadratic normal form. -/
theorem representative_decomposition
    (C : CauchyScalarCertificate) (e : Expr) :
    qmk e =
      add (ofR (normalize e).re)
        (mul (ofR (normalize e).im) imag) := by
  apply Quotient.sound
  change
    normalize e =
      normalize
        (.add (.coeff (normalize e).re)
          (.mul (.coeff (normalize e).im) .generator))
  rw [normalized_coordinate_expression C
      (normalize e).re (normalize e).im]

/-- P/Q-07: every quotient value has a real/imaginary decomposition. -/
theorem decomposition
    (C : CauchyScalarCertificate) (z : QuotientCandidate) :
    ∃ a b : RCBOMA, z = add (ofR a) (mul (ofR b) imag) := by
  refine Quotient.inductionOn z ?_
  intro e
  exact ⟨(normalize e).re, (normalize e).im,
    representative_decomposition C e⟩

/-- P/Q-08: quotient equality retains unique real/imaginary coordinates. -/
theorem decomposition_unique
    (C : CauchyScalarCertificate)
    {a b a' b' : RCBOMA}
    (h : add (ofR a) (mul (ofR b) imag) =
      add (ofR a') (mul (ofR b') imag)) :
    a = a' ∧ b = b' := by
  have hn :
      normalize (.add (.coeff a) (.mul (.coeff b) .generator)) =
      normalize (.add (.coeff a') (.mul (.coeff b') .generator)) :=
    Quotient.exact h
  rw [normalized_coordinate_expression C a b,
      normalized_coordinate_expression C a' b'] at hn
  exact ⟨congrArg NormalForm.re hn,
         congrArg NormalForm.im hn⟩

/-- P/Q-09: the quotient generator cannot equal an embedded real. -/
theorem imag_not_real
    (C : CauchyScalarCertificate) :
    ¬ ∃ a : RCBOMA, imag = ofR a := by
  rintro ⟨a, ha⟩
  have hn : normalize .generator = normalize (.coeff a) :=
    Quotient.exact ha
  have h : rCOne = rCZero := congrArg NormalForm.im hn
  exact C.nontrivial h.symm

end BOMA.C.StageTwo.QExpression015
